# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019-11-01
-------------------------------------------------
   Change Activity:
                   2019-11-01:
-------------------------------------------------
"""

from flask import request, jsonify
from . import yq_gmd
from .db_op import get_gmd_by_patient
from .utils import get_birthday, encode_base64, decode_base64
import logging
import json
from jktj.jktj import tjAssert, loginByUserNamePwd, loadExam, getUserByRealName, getDiseaseByName, saveExamData, \
    loginAssems, cancelLoginAssems, getUserIdByRealName

from jktj.tjsaveexam import initSaveExam, addElementResult, addDisease, addPosReport, getElementAssemByCode

from .uploadreport import upload_report


from . import appconfig
import re
import chardet
from datetime import datetime

log = logging.getLogger(__name__)

@yq_gmd.route('/test',methods=['POST'])
def test():
    log.info('header:{}'.format(request.headers))
    log.info('测试收到的数据:{}'.format(request.data))
    log.info('测试收到的数据json:{}'.format(request.json))
    log.info('测试收到的数据form:{}'.format(request.form))
    try:
       # r = chardet.detect(request.data)
       #
       # return r['encoding']

       return str(request.data,encoding='utf8')
    except Exception as e:
        return repr(e)


@yq_gmd.route('/testimg')
def testimg():
    # 开始读取图像
    try:
        with open('E:/VMShare/2.jpg', 'rb') as f:
            data = f.read()
            s = encode_base64(data)
            return {
                'data': s
            }


    except Exception as e:
        return repr(e)


@yq_gmd.route('/get')
def get_gmd():
    gmd_list = []
    paitent_id = request.args.get('patientid', None)
    try:
        if not paitent_id:
            raise Exception('获取到无效的病人ID')
        gmds = get_gmd_by_patient(paitent_id)
        for gmd in gmds:
            gmd_list.append(
                {
                    'Age': gmd.Age,
                    'Birthday': get_birthday(gmd.Birthday, gmd.Age).strftime('%Y/%m/%d'),
                    'Diagnosis': None,
                    'DiagnosticianDoctor': None,
                    'ExamDepartment': None,
                    'ExamDoctor': None,
                    'Gender': 0 if gmd.Gender == '男' else 1,
                    'Height': None if not gmd.Height else float(gmd.Height),
                    'Name': gmd.NAME,
                    'PatientID': str(gmd.PatientID),
                    'Phone': None,
                    'RequestDate': gmd.RequstDate.strftime('%Y/%m/%d'),
                    'RequestDepartment': '体检中心',
                    'RequestDoctor': gmd.RequestDoctor,
                    'Weight': None if not gmd.Weight else float(gmd.Weight)

                }
            )
    except Exception as e:
        log.error('获取客户的骨密度记录失败！{}'.format(paitent_id))
        log.exception(e)
    finally:
        return jsonify(gmd_list)


@yq_gmd.route('/save', methods=['POST'])
def save_gmd():
    # 获取参数
    r = {
        "Msg": None,
        "Status": "SUCCESS"
    }

    log.info('开始解析骨密度参数...')
    try:

        # print(request.json)
        gmd = json.loads(str(request.data, encoding='utf-8'))
        log.info('获取到要保存的骨密度数据:{}'.format(gmd))
        patient_id = gmd.get('patientID')
        t = gmd.get('t')
        z = gmd.get('z')
        examDoctor = gmd.get('examDoctor')
        check_result = gmd.get('checkResultStr')
        log.info(
            '获取到patient_id:{}  t值:{}  z值:{} 检查结果:{} examDoctor:{}'.format(patient_id, t, z, check_result, examDoctor))

        exam_username = appconfig['JK_EXAM_USERNAME']
        exam_password = appconfig['JK_EXAM_PASSWORD']
        log.info('开始尝试登录体检系统，用户名:{} 密码:{}'.format(exam_username, exam_password))
        result = tjAssert(loginByUserNamePwd(exam_username, exam_password))
        log.info(result['msg'])

        # 获取报告医生的ID
        reporterId = getUserIdByRealName(examDoctor, appconfig['PACS_USE_EXAM_DOCTOR'], 'gmd')
        log.info("获取报告医生ID为:{}".format(reporterId))
        log.info('开始保存骨密度数据...')

        # 获取诊断医生ID

        department_id = appconfig['DEPARTMENT']
        assemdIds = appconfig['ASSEM_ID']
        order_id = patient_id

        log.info('开始根据科室、项目组、预约号获取体检信息，科室ID:{} 预约号:{}  项目组ID:{}'.format(department_id, order_id, assemdIds))
        msg = tjAssert(loadExam(dept=department_id, orderId=patient_id, filterAssemIds=assemdIds))
        exam = msg['msg']
        # 初始化保存数据
        saveExam = initSaveExam(exam, department_id, reporterId, reporterId)

        # 小项结果
        fs = {'3837': str(t), '3838': str(z)}
        addElementResult(saveExam, exam=exam, opId=reporterId, **fs)


        log.info('获取诊断信息:{}'.format(check_result))
        summary =check_result
        log.info('获取结论:{}'.format(summary))

        writeSymbol = None
        diseaseCode = None
        if summary.find('骨量正常') >= 0:
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

        # 开始提交分科结果
        examData = json.dumps(saveExam)
        log.info(examData)
        log.info('开始提交分科结果...')
        result = tjAssert(saveExamData(examData))
        log.info(result['msg'])

        # 开始上传图像
        img = gmd.get('image')
        if img:
            log.info('开始上传图像报告...')
            upload_report(order_id=patient_id,
                          department_id=department_id,
                          pacs_assem_id=assemdIds,
                          pacs_assem_name='超声骨密度',
                          reporter_id=reporterId,
                          report_base64=img,
                          report_date=datetime.now()
                          )

        r['Msg'] = '上传成功'
    except Exception as e:
        r['Msg'] = "上传失败!{}".format(repr(e))
        log.error('上传数据失败')
        log.exception(e)

    finally:
        log.info('返回数据:{}'.format(r))
        return jsonify(r)
