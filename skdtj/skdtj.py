# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     skdtj
   Description :
   Author :       wdh
   date：          2019/2/14
-------------------------------------------------
   Change Activity:
                   2019/2/14:
-------------------------------------------------
"""

# import datetime
import requests
from requests.exceptions import RequestException
from skdtj.tjexception import TJException, TJConnectionException
from pypinyin import lazy_pinyin
import json
import re
import logging

log = logging.getLogger(__name__)

HOST_CONST = None

_session = requests.Session()

_init_host = None


def initHost(host):
    global _init_host
    _init_host = host


def _getUrl(action):
    if action:
        return "%s/%s" % (_init_host, action)
    else:
        return _init_host


def _getReturn(success, msg, canNext=True):
    """
    统一返回
    :param success:
    :param msg:
    :param canNext:
    :return:
    """
    return {"success": success, "msg": msg, "canNext": canNext}


def _tansResult(data, dataField):
    """
    判断结果是否正常
    :param data:
    :return:
    """
    if data:
        if hasattr(data, 'keys'):
            if "success" in data.keys():
                if dataField:
                    return _getReturn(data['success'], data[dataField])
                else:
                    return _getReturn(data['success'], data['msg'] if data['msg'] else data['result'])
            else:
                return _getReturn(True, data)
        else:
            return _getReturn(True, data)
    else:
        return _getReturn(True, data)


def _dealException(ex, res):
    """
    统一处理异常
    :param ex:
    :return:
    """
    if ex:
        if isinstance(ex, RequestException) or (hasattr(ex, 'doc') and (ex.doc.find('请重新登陆') >= 0)):
            return _getReturn(False, repr(ex) if not hasattr(ex, 'doc') else ex.doc, False)
        else:
            if res:
                return _getReturn(False, res.text)
            else:
                return _getReturn(False, repr(ex))


def _post(action, dataField=None, **kwargs):
    """
    通用pos方法
    :param action:
    :param kwargs:
    :return:
    """
    r = None
    try:
        if action is None:
            raise Exception("action名字不能为空")
        r = _session.post(url=_getUrl(action), data=kwargs)
        data = r.json()
        return _tansResult(data, dataField)
    except Exception as e:
        return _dealException(e, r)


def login(name, password):
    """
    用户名和密码进行登录
    :return:
    """
    # params = {'name':USERNAME_CONST,'password':PASSWORD_CONST}
    # return _post('operator_checkLogin',**params)
    params = {'name': name, 'password': password}
    return _post('user_checkLogin', **params)


# http://lanshankeji.vicp.net:9090/subarea/personalReservation_updateReserveArrival
# 参数：reserveNo=1210513
#    arrivalDate=2019-05-11 09:11:20

def update_arrival(rese_id, arrrival_time):
    """
    尝试报道
    :param rese_id:
    :param rese_date:
    :return:
    """
    params = {
        'reserveNo': rese_id,
        'arrivalDate': arrrival_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return _post('personalReservation_updateReserveArrival', **params)


def get_person_info(rese_id):
    params = {
        'reseId': rese_id
    }
    return _post('workstationMain_getPersonalInfo', **params)


def get_exam_result(rese_id, dept_id):
    params = {
        'reseId': rese_id,
        'deptId': dept_id,
        'ignoreSubarea': True
    }
    return _post('workstationMain_getExamResultForGrid', **params)


def get_exam_item_result(rese_id, dept_id, item_com_ids):
    params = {
        'reseId': rese_id,
        'deptId': dept_id,
        'itemComIds': item_com_ids,
        'ignoreUserSelect': True,
        'ignoreItemGroupLogin': True,
        'ignoreSubarea': True
    }
    return _post('workstationMain_getItemAndResultForGrid', **params)


def save_exam(b_exam_result, b_exam_item_result, b_summaries, deleted_summaries):
    params = {
        'dataExamResult': json.dumps(b_exam_result, ensure_ascii=False),
        'dataItemResult': json.dumps(b_exam_item_result, ensure_ascii=False),
        'dataItemComSummary': json.dumps(b_summaries, ensure_ascii=False),
        'dataItemComSummaryIds': deleted_summaries,
        'isBarCodeId': False
    }
    return _post('workstationMain_saveExaminationResult', **params)


# workstationMain_getItemComSummaryForGrid
def get_item_com_summary(rese_id, dept_id, item_com_ids):
    params = {
        'reseId': rese_id,
        'deptId': dept_id,
        'ignoreUserSelect': True,
        'ignoreItemGroupLogin': True,
        'itemComIds': item_com_ids,
        'ignoreSubarea': True
    }
    return _post('workstationMain_getItemComSummaryForGrid', **params)


def saveOrder(params):
    return _post('personalReservation_savePersonalReservationInfo', dataField='str', **params)


def updateOrderDate(orderId, orderExamDate):
    """
    更新团检预约日期
    :param orderId:
    :param orderExamDate:
    :return:
    """
    params = {
        'reserveNo': orderId,
        'reserveDate': orderExamDate
    }
    return _post('personalReservation_updateReserveDate', **params)


def pay(orderId, paymentAmount, payGroupIds, payId, payType):
    """
    小程序在线支付
    :param orderId:
    :param paymentAmount:
    :param groupdIds:
    :param payId:
    :param payType:
    :return:
    """
    params = {
        'reservation': orderId,
        'paymentAmount': paymentAmount,
        'itemCombinationIds': payGroupIds,
        'payId': payId,
        'payType': payType
    }

    return _post('personalCharge_saveSmallProgramPay', **params)


def queryCanDeleteOrder(orderId):
    params = {'personalReservationModel.id': orderId, 'limit': 100}
    return _post('personalReservationSKDTJ_getPersonReservated', **params)


def deleteOrder(orderId):
    params = {'selectKeys': orderId}
    return _post('personalReservationSKDTJ_delete', **params)


def get_user_info(prefix, realname):
    params = {
        'userLoginName': '{}_{}'.format(prefix, ''.join(lazy_pinyin(realname))),
        'userRealName': realname
    }
    return _post('user_getUserInfo', **params)


def get_disease(disease_name):
    params = {
        'name': disease_name
    }
    return _post('disease_getDiseaseByName', **params)


def build_exam_result(exam_result_dict, positive_content, operator_id, reporter_id, audit_doctor_id):
    """
    构建重大阳性
    :return:
    """
    if exam_result_dict['positiveAuditStatus'] == '未审':
        exam_result_dict['additionalOperator'] = operator_id if operator_id is not None else reporter_id
        exam_result_dict['userId'] = reporter_id if reporter_id is not None else audit_doctor_id
        exam_result_dict['ifPositive'] = '是' if positive_content and positive_content != '无' else '否'
        exam_result_dict['positiveContent'] = positive_content if positive_content and positive_content != '无' else ''
        exam_result_dict['saveStatus'] = '提交'
    return exam_result_dict


def build_exam_item_result(exam_item_result_list, items_result_dict, operator_id, reporter_id, audit_doctor_id):
    """
    构建项目结果
    :param exam_item_result_dict:
    :param items_result_dict:
    :param operator_id:
    :param reporter_id:
    :param audit_doctor_id:
    :return:
    """
    r = []
    for exam_item in exam_item_result_list:
        if exam_item['rowType'] == 'item':
            key = str(exam_item['itemId'])
            if not key in items_result_dict.keys():
                raise TJException(
                    '在中间结果表中，没有查询到小项id:{} 项目名称:{}  对照码:{} 的项目结果'.format(exam_item['itemId'], exam_item['name'],
                                                                        exam_item['extSysCode']))

            item_result = items_result_dict[key]
            # if not item_result.REPORT_DIAGNOSE:  # 项目结果
            #     raise TJException(
            #         '在中间结果表中，小项id:{} 项目名称:{} 对照码:{} 的项目结果为空'.format(exam_item['itemId'], exam_item['name'],
            #                                                         exam_item['extSysCode']))

            exam_item[
                'result'] = item_result.REPORT_DIAGNOSE if item_result.REPORT_DIAGNOSE else item_result.REPORT_RESULT
            exam_item['additionalOperatorId'] = reporter_id if reporter_id is not None else operator_id
            exam_item['userId'] = audit_doctor_id if audit_doctor_id is not None else reporter_id
            r.append(exam_item)
    return r


def _get_summary(com_id, disease_content, disease_name, if_selfwrite):  # 01-疾病ID、02-自写诊断、03-默认小结、04-放弃
    r = {
        'rId': None,
        'itemgroupSummaryId': None,
        'itemComId': com_id,
        'mergeWord': None,
        'diseaseContent': disease_content,
        'diseaseName': disease_name,
        'ifSelfwrite': if_selfwrite,
        'doubt': False,
        'diseasePositions': '',
        'mergeWord': disease_name,
        'resultContent': ''
    }
    return r


def build_exam_summary(item_com_summary_dict, item_com_summary, com_id, operator_id, reporter_id, audit_doctor_id,
                       item_result_list):
    deletes = []
    details = item_com_summary_dict[com_id]['itemComSummaryDetatiles']  # 获取小接
    for detail in details:
        if (detail['rId'] is not None) and (detail['rId'] != 0):
            deletes.append(str(detail['rId']))
    details.clear()

    default_value = item_com_summary_dict[com_id]['defaultValue']

    summary_dict = item_com_summary_dict[com_id]

    summary_dict['saveStatus'] = '提交'
    summary_dict['userId'] = audit_doctor_id if audit_doctor_id is not None else reporter_id

    # 增加新的小节
    if item_com_summary and item_com_summary.strip() == default_value:
        details.append(_get_summary(com_id, default_value, default_value, '03'))
    else:
        sumaries = re.split(r'\r\n|;', item_com_summary) if item_com_summary else item_result_list
        log.info('拆分后的结论为:{}'.format(sumaries))
        for summary in sumaries:
            if summary and summary.strip():
                # 判断是否为默认小结
                if summary.find('未见明显异常') >= 0 or summary.find('无明显异常') >= 0:
                    details.append(_get_summary(com_id, summary, summary, '03'))
                    continue

                log.info('将结论:【{}】在体检数据库进行对比...'.format(summary))
                r = get_disease(summary.strip())
                disease_dict = r['msg']
                if 'id' in disease_dict:
                    details.append(_get_summary(com_id, disease_dict['id'], summary, '01'))
                else:
                    details.append(_get_summary(com_id, summary, summary, '02'))

    return (item_com_summary_dict, ','.join(deletes))


def build_lis(exam_item_list, lis_results_dict, res_id, com_id, reporter_id, auditor_id):
    lis_items_list = []
    for item in exam_item_list:
        itemId = item['itemHeaId']
        itemName = item['itemHeaName']
        extSysCode = item['extSysCode']

        if extSysCode not in lis_results_dict.keys():
            raise Exception(
                '获取到 项目组id:{}  项目id:{} 项目名称:{} 外部对照码:{} 在项目结果中无法找到'.format(com_id, itemId,
                                                                           itemName, extSysCode))

        lis_result = lis_results_dict[extSysCode]

        item_dict = {
            'reserveId': res_id,
            'resultType': item['resultType'],
            'ferenceLowerLimit': item['ferenceLowerLimit'] if item['ferenceLowerLimit'] is not None else 0,
            'ferenceUpperLimit': item['ferenceUpperLimit'] if item['ferenceUpperLimit'] is not None else 0,
            'recvYsId': reporter_id if reporter_id is not None else auditor_id,
            'checkYsId': auditor_id if auditor_id is not None else reporter_id,
            'checkTjjg': lis_result['result'],
            'igId': com_id,
            'itemId': item['itemId'],
            'reportingMark': '0'
        }
        lis_items_list.append(item_dict)
    return lis_items_list


def save_lis(lis_result_list, department_id):
    log.info('准备保存的  科室id:{}  lis结果:{}'.format(department_id, lis_result_list))
    params = {
        'deptId': department_id,
        'dataExamResult': json.dumps(lis_result_list, ensure_ascii=False),
        'ignoreItemResultDeviceUpdate': True
    }
    return _post('workstationLis_saveOrUpdateResult4Lis', **params)


def download_pdf(rese_id):
    """
    下载报道pdf文件
    :param rese_id:
    :return:
    """
    try:
        params = {
            'reserveId': rese_id
        }
        r = _session.post(_getUrl('personalReport_apiGetReportPdf'), data=params)
        contenttype = r.headers['Content-Type']
        log.info('获取到文件的Content-Type:{}'.format(contenttype))
        if contenttype and contenttype.find('pdf') >= 0:
            return r
        else:
            data = r.json()
            return tjAssert(_tansResult(data, None))
    except Exception as e:
        return _dealException(e, r)


def tjAssert(result, extraMsg=None):
    """
    一个判断体检api执行的断言，如果失败，则抛出异常
    :param result:
    :return:
    """
    if isinstance(result, dict):
        if result['success']:
            return result
        else:
            msg = result['msg']  # if hasattr(result,'msg') else result['message']
            if extraMsg is not None:
                msg = '[{}]{}'.format(extraMsg, msg)
            canNext = result['canNext']
            if not canNext:
                raise TJConnectionException(msg)
            else:
                raise TJException(msg)
    else:
        raise TJException("近回值无效" + extraMsg if extraMsg is not None else '')
