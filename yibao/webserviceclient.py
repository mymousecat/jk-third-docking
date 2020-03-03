# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     webserviceclient
   Description :
   Author :       wdh
   date：          2019/7/17
-------------------------------------------------
   Change Activity:
                   2019/7/17:
-------------------------------------------------
"""
from . import appconfig
import logging
from suds.client import Client
from bs4 import BeautifulSoup
from .requestdata import RequestData
from .util import encode_base64, decode_base64
from .err import InValidException, NotFoundException, InvokeException

log = logging.getLogger(__name__)


def buildRequestData(msg_no):
    return RequestData(
        hosp_id=appconfig['HOSP_ID'],
        hosp_name=appconfig['HOSP_NAME'],
        msg_no=msg_no,
        grant_id=appconfig['GRANTID'],
        oper_id=appconfig['UPLOAD_OPER_ID'],
        oper_name=appconfig['UPLOAD_OPER_NAME']
    )


EXAM_YEAR = appconfig['EXAM_YEAR']
WEBSERVICE_WSDL = appconfig['WEBSERVICE_WSDL']


def _deal_response(r):
    soap = BeautifulSoup(r, features='xml')
    data = soap.find('RESPONSEDATA')
    if not data:
        raise InValidException('无效的回应消息,{}'.format(r))
    response_dict = dict([(item.name, item.text) for item in data.find_all()])
    if 'RETURNNUM' not in response_dict.keys():
        raise InValidException('无效的回应消息,{}'.format(r))
    if response_dict['RETURNNUM'] == '-1':
        raise InvokeException('调用Webservice出错，错误消息:{}'.format(response_dict['ERRORMSG']))
    return response_dict


def _invoke(inParam):
    inP = encode_base64(inParam)
    client = Client(WEBSERVICE_WSDL)
    r = decode_base64(client.service.ybjkinterface(inP))
    log.info('收到医保系统的回应:{}'.format(r))
    return _deal_response(r)


def get_info_from_yibao(username, cert_id):
    request = buildRequestData('BI411005')
    request.buildInput().addName(username).addIdCard(cert_id).addExamYear(EXAM_YEAR)
    response = _invoke(request.tostring())
    if 'OUTPUT' not in response.keys():
        raise NotFoundException('没有在医保系统中，找到用户名:{} 身份证号:{} 的体检人信息!'.format(username, cert_id))
    return response


def upload_exam(requestdata):
    str_request = requestdata.tostring()
    log.info('上始上传体检结果信息:{}'.format(str_request))
    response = _invoke(str_request)
    return response
