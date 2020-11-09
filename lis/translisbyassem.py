# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     translisbyassem
   Description :
   Author :       wdh
   date：          2019/8/14
-------------------------------------------------
   Change Activity:
                   2019/8/14:
-------------------------------------------------
"""

import json
import re
from jktj.tjexception import TJException
from jktj.jktj import loginByUserNamePwd, tjAssert, loadExam, getUserIdByRealName, saveLisExamData
import logging
from . import appconfig

log = logging.getLogger(__name__)


# def _get_login_name(realname):
#     return 'yh_{}'.format(''.join(lazy_pinyin(realname)))


def _is_number(s):
    try:
        if s is not None:
            float(s)
            return True
    except ValueError:
        pass


def _get_opid(lisResult):
    opName = lisResult.OPERATOR_NAME  # 报告医生
    auditName = lisResult.AUDIT_NAME  if lisResult.AUDIT_NAME is not None else lisResult.OPERATOR_NAME  # 审核医生，如果审核医生为空，则使用报告医生

    log.info('获取到报告医生:{}  审核医生:{}'.format(opName, auditName))

    opId = getUserIdByRealName(opName, False, 'lis')

    log.info("获取报告医生id:{}  用户名:{}".format(opId, opName))

    if not auditName:
        raise TJException('没有发现有效的审核医生')

    auditId = getUserIdByRealName(auditName, False, 'lis')

    log.info("获取审核医生id:{}  用户名:{}".format(auditId, auditName))
    return opId, auditId


def transLisByAssem(departmentId, order_id, assemId, lis_result_dict):
    """
    上传LIS数据到体检系统中
    :param departmentId: 科室ID
    :param assemId:项目组ID
    :lis_result_dict:项目结果字典
    :return:
    """

    lis_result_key_set = set()
    for key in lis_result_dict.keys():
        lis_result_key_set.add(key)

    # 开始尝试登录到体检系统
    log.info('开始尝试登录体检系统，用户名:{} 密码:{}'.format(appconfig['JK_EXAM_USERNAME'], appconfig['JK_EXAM_PASSWORD']))
    result = tjAssert(loginByUserNamePwd(appconfig['JK_EXAM_USERNAME'], appconfig['JK_EXAM_PASSWORD']))
    log.info('开始根据科室、项目组、预约号获取体检信息，科室ID:{} 预约号:{}  项目组ID:{}'.format(departmentId, order_id, assemId))
    msg = tjAssert(loadExam(dept=departmentId, orderId=order_id, filterAssemIds=assemId))

    log.info('开始检查以及组装体检项目...')

    exam = msg['msg']

    assem = exam['assems'][0]

    elements = assem['elements']

    # 使用外键组成项目字典
    examElementDict = {}
    examElementSet = set()

    for element in elements:
        extCode = element['extSysControlCode']
        if not extCode:
            raise TJException('项目名：{} 的系统对照为空'.format(element['elementName']))

        # 开始分割项目对照码，一个小项，可以有多个对照码，使用,，|^，进行分割
        keys = re.split(r',|，|\^|\|', extCode)
        for key in keys:
            if key:
                code = key.strip()
                if code:
                    examElementDict[code] = element
                    examElementSet.add(code)

    # 计算体检检查项目及lis项目结果列表的交集
    both_set = set.intersection(examElementSet, lis_result_key_set)

    # 开始对小项进行标记
    for code in both_set:
        examElementDict[code]['bingo'] = True

    errMsgs = []
    log.info('开始检查哪些项目，在HIS中没有结果...')
    # 开始检查哪些项目没有结果
    for element in elements:
        if 'bingo' not in element.keys():
            errMsg = '在LIS提供的项目列表中，未发现项目id:{} 项目名:{} 项目对照:{}的项目'.format(element['elementId'],
                                                                        element['elementName'],
                                                                        element['extSysControlCode'])
            errMsgs.append(errMsg)

    if len(errMsgs) > 0:
        raise TJException(';'.join(errMsgs))

    log.info('开始生成LIS体检项目...')

    lisDatas = {

        'orderId': order_id,
        'elementAssemId': assemId,
        'departmentId': departmentId,
        'sampleOpId': None,  # 报告人
        'opId': None,  # 审核人
        'items': []
    }

    c = 0

    item_results = []

    for code in both_set:
        try:
            examElement = examElementDict[code]

            hisLisElement = lis_result_dict[code]

            if c == 0:
                log.info('用于获取项目结果及操作员的记录ID:{}'.format(hisLisElement.ID))
                sampleOpId, opId = _get_opid(hisLisElement)
                lisDatas['sampleOpId'] = sampleOpId
                lisDatas['opId'] = opId

            lisElement = {}
            lisElement['elementId'] = examElement['elementId']
            lisElement[
                'checkElementResult'] = hisLisElement.CONTENT_RESULT.strip() if hisLisElement.CONTENT_RESULT else None

            lisElement['ferenceLower'] = hisLisElement.FERENCE_LOWER_LIMIT if _is_number(
                hisLisElement.FERENCE_LOWER_LIMIT) else 0

            lisElement['ferenceUpper'] = hisLisElement.FERENCE_UPPER_LIMIT if _is_number(
                hisLisElement.FERENCE_UPPER_LIMIT) else 0

            lisElement['unit'] = hisLisElement.RESULT_UNIT
            lisElement['resultType'] = examElement['resultType']
            lisElement['referenceType'] = '1'  # e['refType']

            # 危机值的标识？
            lisElement['criticalValuesSymbol'] = hisLisElement.CRITICAL_VALUES_SYMBOL

            if hisLisElement.POSITIVE_SYMBOL == '↓':
                lisElement['positiveSymbol'] = '低'
            elif hisLisElement.POSITIVE_SYMBOL == '↑':
                lisElement['positiveSymbol'] = '高'
            else:
                lisElement['positiveSymbol'] = None
            lisDatas['items'].append(lisElement)

            # 项目的结果值列表保存，作为将来的参考，结构为 项目名称^项目结果^审核时间
            item_results.append('{}^{}^{}'.format(hisLisElement.LIS_ELEMENT_NAME,
                                                  hisLisElement.CONTENT_RESULT,
                                                  hisLisElement.AUDIT_DATE.strftime(
                                                      '%Y-%m-%d %H:%M:%S') if hisLisElement.AUDIT_DATE else None
                                                  ))



        finally:
            c += 1

    log.info('开始上传LIS结果数据...')

    examData = json.dumps(lisDatas)
    log.info(examData)

    log.info("开始保存LIS结果....")
    result = tjAssert(saveLisExamData(examData))
    log.info(result['msg'])

    return '\n'.join(item_results)
