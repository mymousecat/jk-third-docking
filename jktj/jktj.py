#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/9/26 17:54


"""

 国瑞体检业务封装

"""
import datetime
import requests
from urllib.parse import urljoin

from requests.exceptions import RequestException
from .tjexception import TJException, TNetException

# HOST_CONST = "http://192.168.10.250"

HOST_CONST = "http://192.168.11.12"

USERNAME_CONST = "third"
PASSWORD_CONST = "1234"

_session = requests.Session()

_init_host = None


def initHost(host):
    global _init_host
    _init_host = host


def _getUrl(action):
    if action:
        return urljoin(HOST_CONST if _init_host is None else _init_host, action)
    else:
        return HOST_CONST if _init_host is None else _init_host


def _getReturn(success, msg, canNext=True):
    """
    统一返回
    :param success:
    :param msg:
    :param canNext:
    :return:
    """
    return {"success": success, "msg": msg, "canNext": canNext}


def _tansResult(data):
    """
    判断结果是否正常
    :param data:
    :return:
    """
    if data:
        if "success" in data.keys():
            return _getReturn(data['success'],
                              data['result'] if 'result' in data.keys() and data['result'] else data['msg'])
        else:
            return _getReturn(True, data)


def _dealException(ex, res):
    """
    统一处理异常
    :param ex:
    :return:
    """
    if ex:
        if isinstance(ex, RequestException):
            return _getReturn(False, repr(ex), False)
        else:
            if res:
                return _getReturn(False, res.text)
            else:
                return _getReturn(False, repr(ex))


def _post(action, **kwargs):
    """
    通用pos方法
    :param action:
    :param kwargs:
    :return:
    """
    r = None
    try:
        if not action:
            raise Exception("action名字不能为空")
        r = _session.post(url=_getUrl(action), data=kwargs)
        data = r.json()
        return _tansResult(data)
    except Exception as e:
        return _dealException(e, r)


def getBirthday(birthday, age):
    if birthday:
        if hasattr(birthday, 'strftime'):
            return birthday.strftime('%Y-%m-%d')
        else:
            return birthday
    else:
        birth = datetime.date.today() - datetime.timedelta(days=365 * age)
        return birth.strftime('%Y-%m-%d')


def login():
    """
    用已配置好的用户名和密码进行登录
    :return:
    """
    # params = {'name':USERNAME_CONST,'password':PASSWORD_CONST}
    # return _post('operator_checkLogin',**params)
    return loginByUserNamePwd(USERNAME_CONST, PASSWORD_CONST)


def loginByUserNamePwd(name, password):
    """
    使用用户名和密码进行登录
    :param name:
    :param password:
    :return:
    """
    params = {'name': name, 'password': password}
    return _post('operator_checkLogin', **params)


def getUserByRealName(realName):
    """
    通过真实姓名查找得到用户对象
    :param realName:用户真实姓名
    :return:
    """
    params = {'realName': realName}
    return _post('operator_getByOperatorRealName', **params)


def getUserInfo(userLoginName, userRealName):
    """
    获取用户信息，如果没有，则创建
    :param userLoginName:
    :param userRealName:
    :return: {"userId":146}
    """
    params = {
        'userLoginName': userLoginName,
        'userRealName': userRealName
    }
    return _post('operator_getUserInfo', **params)


from pypinyin import lazy_pinyin


def _get_login_name(realname, prefix):
    return '{}_{}'.format(prefix, ''.join(lazy_pinyin(realname)))


def getUserIdByRealName(userRealName, useExamDoctor, prefix):
    """
    根据用户的真实姓名，从体检中获取用户id
    :param userRealName:
    :param useExamDoctor:
    :param prefix:
    :return:
    """
    if useExamDoctor:  # 如果使用体检系统中已存在的医生
        result = tjAssert(getUserByRealName(userRealName))
        return result['msg']['id']
    else:  # 如果不使用体检系统已存在的医生，则新增
        pf = prefix if prefix else 'ext'
        loginname = _get_login_name(userRealName, pf)
        result = tjAssert(getUserInfo(loginname, userRealName))
        return result['msg']['userId']


def loginAssems(orderId, assemIds, opId):
    """
    项目组登入操作

    :param orderId:
    :param assemIds:
    :param opId:
    :return:
    """
    params = {'orderId': orderId, 'assemIds': assemIds, 'opId': opId}
    return _post('exam_assemLogin', **params)


def cancelLoginAssems(orderId, departmentId, assemIds, opId):
    """
    项目组取消登入操作
    :param orderId:
    :param departmentId:
    :param assemIds:
    :param opId:
    :return:
    """
    params = {'orderId': orderId, 'assemIds': assemIds, 'opId': opId, 'deptId': departmentId}
    return _post('exam_assemLoginCancel', **params)


def loadExam(dept, orderId, noAssemLogin=True, noSelectAssem=True, filterAssemIds=None):
    """
    获取体检项目
    :param dept:
    :param orderId:
    :param noAssemLogin:
    :param noSelectAssem:
    :return:
    """
    params = {'deptId': dept, 'orderId': orderId, 'noSelectAssem': noSelectAssem, 'noAssemLogin': noSelectAssem}

    if filterAssemIds:
        params['filterAssemIds'] = filterAssemIds

    return _post('exam_loadExam', **params)


def getDiseaseByName(diseaseName):
    """
    根据疾病名称，来获取疾病
    :param diseaseName:
    :return:
    """
    params = {'name': diseaseName}
    return _post('disease_getDiseaseByName', **params)


def saveExamData(examData):
    """
    保存分科结果
    :param examData:
    :return:
    """
    params = {'examData': examData}
    return _post('exam_saveExamData', **params)


def saveLisExamData(examData):
    """
    保存LIS结果
    :param examData:
    :return:
    """
    params = {'examData': examData}
    return _post('lisData_saveLisExamData', **params)


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
            msg = result['msg']
            if extraMsg is not None:
                msg = '[{}]{}'.format(extraMsg, msg)

            canNext = result['canNext']
            if canNext:
                raise TJException(msg)
            else:
                raise TNetException(msg)
    else:
        raise TJException("近回值无效" + extraMsg if extraMsg is not None else '')


def saveOrder(params):
    return _post('apiOrder_orderSave', **params)


def deleteOrder(orderId):
    params = {'orderId': orderId}
    return _post('apiOrder_orderDelete', **params)


def updateOrderDate(orderId, orderExamDate):
    """
    更新团检预约日期
    :param orderId:
    :param orderExamDate:
    :return:
    """
    params = {
        'orderId': orderId,
        'orderDate': orderExamDate
    }
    return _post('apiOrder_orderDateUpdate', **params)


def download_pdf(orderId):
    """
    下载报道pdf文件
    :param rese_id:
    :return:
    """
    try:
        params = {
            'orderId': orderId
        }
        r = _session.post(_getUrl('apiReport_report4Person'), data=params)
        contenttype = r.headers['Content-Type']
        # log.info('获取到文件的Content-Type:{}'.format(contenttype))
        if contenttype and contenttype.find('pdf') >= 0:
            return r
        else:
            data = r.json()
            return tjAssert(_tansResult(data, None))
    except Exception as e:
        return _dealException(e, r)

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

    return _post('apiCharge_weChatMiniProgramPay', **params)



if __name__ == "__main__":
    print(getBirthday('2002-10-3', 23))
