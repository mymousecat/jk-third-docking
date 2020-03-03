# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     trans
   Description :
   Author :       wdh
   date：          2019/7/30
-------------------------------------------------
   Change Activity:
                   2019/7/30:
-------------------------------------------------
"""

import logging
import json
import re
from . import appconfig
from .db_op import get_assem_by_map, get_assem_by_id
from .err import NotFoundException, InvalidMultiException, InvalidDialogException, InvalidOpTypeException
from jktj.jktj import tjAssert, loginByUserNamePwd, loadExam, getUserByRealName, getDiseaseByName, saveExamData, \
    loginAssems, cancelLoginAssems, getUserIdByRealName
from jktj.tjsaveexam import initSaveExam, addElementResult, addDisease, addPosReport, getElementAssemByCode
from .uploadreport import upload_report
import datetime

log = logging.getLogger(__name__)


def _common_fun(pacs_assem_id):
    log.info('开始通过PACS项目组ID:{}从体检系统中，获取映射的体检项目组ID及科室ID信息.'.format(pacs_assem_id))

    assems = None
    if appconfig['MAP_CODE_IS_ASSEM_ID']:
        assems = get_assem_by_id(pacs_assem_id)
    else:
        assems = get_assem_by_map(appconfig['DEPARTMENTS_RANGE'], pacs_assem_id)

    if len(assems) == 0:
        raise NotFoundException('pacs项目组对照码:{}，在体检系统中没有找到相应的项目组与其对应.'.format(pacs_assem_id))

    log.info('使用PACS项目组ID:{}找到{}条项目组映射.'.format(pacs_assem_id, len(assems)))
    department_id_set = set([assem.department_id for assem in assems])
    if len(department_id_set) > 1:
        raise InvalidMultiException('pacs项目组对照码:{}对应了多个科室的项目组，这是无效的，多个科室id:{}'.format(pacs_assem_id, department_id_set))
    assem_id_list = [str(assem.id) for assem in assems]
    assem_name_list = [assem.name for assem in assems]
    log.info('获取到项目组id:{} 对应的项目组名字:{}'.format(assem_id_list, assem_name_list))
    # 开始尝试登录到体检系统
    exam_username = appconfig['JK_EXAM_USERNAME']
    exam_password = appconfig['JK_EXAM_PASSWORD']
    log.info('开始尝试登录体检系统，用户名:{} 密码:{}'.format(exam_username, exam_password))
    result = tjAssert(loginByUserNamePwd(exam_username, exam_password))
    log.info(result['msg'])
    return list(department_id_set)[0], ','.join(assem_id_list)


def trans_pacs_result(order_id, pacs_assem_id, pacs_assem_name, report_diagnose, report_result, positive_content,
                      report_url, reporter,
                      audit_doctor, report_date):
    """
    根据预约号、PACS项目组ID，传输pacs结果到体检系统
    :param order_id:
    :param pacs_element_id:
    :return:
    """
    department_id, assemdIds = _common_fun(pacs_assem_id)

    # 获取报告医生的ID
    reporterId = getUserIdByRealName(reporter, appconfig['PACS_USE_EXAM_DOCTOR'], 'pacs')
    log.info("获取报告医生ID为:{}".format(reporterId))

    # 获取审核医生ID
    confirmId = getUserIdByRealName(audit_doctor, appconfig['PACS_USE_EXAM_DOCTOR'], 'pacs')
    log.info("获取审核者医生ID为:{}".format(confirmId))

    log.info('开始根据科室、项目组、预约号获取体检信息，科室ID:{} 预约号:{}  项目组ID:{}'.format(department_id, order_id, assemdIds))
    msg = tjAssert(loadExam(dept=department_id, orderId=order_id, filterAssemIds=assemdIds))
    exam = msg['msg']
    # 初始化保存数据
    saveExam = initSaveExam(exam, department_id, confirmId, reporterId)
    # 小项结果
    fs = {'others': report_result}
    addElementResult(saveExam, exam=exam, opId=reporterId, **fs)
    # 结论部分，开始拆分结论
    log.info('获取结论...')
    if not report_diagnose:
        raise InvalidDialogException('结论不能为空')
    summaries = re.split(r'\;|；|\r|\n|\r\n|[\d]+\.', report_diagnose)
    for s in summaries:
        summary = re.sub(r'^[\d]+\.', '', s.strip())
        if len(summary) == 0:
            continue
        log.info('获取结论:{}'.format(summary))

        writeSymbol = None
        diseaseCode = None
        if summary.find('未见异常') >= 0 or summary.find('未见明显异常') >= 0 or summary.find('未见确切异常') >= 0:
            writeSymbol = '03'
        else:
            result = getDiseaseByName(summary)
            if result is None:
                writeSymbol = '02'
            else:
                writeSymbol = '01'
                diseaseCode = result['msg']['id']
        log.info("获取诊断方式:{},疾病名称:{},疾病id:{}".format(writeSymbol, summary, diseaseCode))
        addDisease(saveExam, exam=exam, deptId=department_id, opId=reporterId, writeSymbol=writeSymbol,
                   diseaseName=summary, diseaseCode=diseaseCode)

    # 重大阳性
    if positive_content:
        if positive_content.strip() != '阴性':
           addPosReport(saveExam, content=positive_content, advice=positive_content, opId=reporterId)

    # 开始提交分科结果
    examData = json.dumps(saveExam)
    log.info(examData)
    log.info('开始提交分科结果...')
    result = tjAssert(saveExamData(examData))
    log.info(result['msg'])

    # 开始传输图像报告
    upload_report(order_id=order_id,
                  department_id=department_id,
                  pacs_assem_id=getElementAssemByCode(exam)['assemId'],
                  pacs_assem_name=pacs_assem_name,
                  reporter_id=reporterId,
                  report_url=report_url,
                  report_date=report_date if report_date else datetime.datetime.now()
                  )


def trans_pacs_reg(order_id, pacs_assem_id, op_type, op_name):
    """
    根据预约号、PACS项目组ID，将项目组进行登入、或取消登入的操作
    :param order_id:
    :param pacs_assem_id:
    :param op_type:
    :param op_name:
    :return:
    """
    department_id, assemdIds = _common_fun(pacs_assem_id)
    # 获取操作者id
    # result = tjAssert(getUserByRealName(op_name))
    # op_id = result['msg']['id']
    # confirmId = getUserIdByRealName(audit_doctor, appconfig['PACS_USE_EXAM_DOCTOR'], 'pacs')
    log.info('获取到技师名字:{}  是否是使用体检系统的用户名:{} '.format(op_name, appconfig['PACS_USE_EXAM_DOCTOR']))
    op_id = getUserIdByRealName(op_name, appconfig['PACS_USE_EXAM_DOCTOR'], 'pacs')
    log.info("获取登记技师ID为:{}".format(op_id))
    result = None
    if op_type == '登记':
        result = tjAssert(loginAssems(order_id, assemdIds, op_id))
    elif op_type == '撤销登记':
        result = tjAssert(cancelLoginAssems(order_id, department_id, assemdIds, op_id))
    else:
        raise InvalidOpTypeException('无效的操作类型OP_TYPE:{},值必须为[登记]或[撤销登记]'.format(op_type))

    log.info(result['msg'])
