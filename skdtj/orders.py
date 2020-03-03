# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     OrderInfo
   Description :
   Author :       wdh
   date：          2019/2/13
-------------------------------------------------
   Change Activity:
                   2019/2/13:
-------------------------------------------------
"""

import datetime
import json


def getAge(birth):
    year = int(birth[0:4])
    return datetime.datetime.now().year - year


class OrderInfo:
    def __init__(self):
        self._params = {}
        self._groups = []

    def addBasicInfo(self, username, certId, birth, sex, mobile, orderExamDate, examType, subarea, customerSource,
                     maritalStatus=None,
                     personId=None, examNo=None, contractGroupId=None, itemPackage=None):
        self._params['personalBaseInfo.username'] = username
        self._params['personalBaseInfo.sex'] = sex
        self._params['personalBaseInfo.birthday'] = birth
        self._params['personalReservation.age'] = getAge(birth)
        self._params['personalBaseInfo.telephone'] = mobile
        self._params['personalReservation.maritalStatus'] = maritalStatus
        self._params['personalBaseInfo.nation'] = '01'
        self._params['personalBaseInfo.certType'] = '1'
        self._params['personalBaseInfo.certId'] = certId
        self._params['personalBaseInfo.photoBase64'] = None
        self._params['personalReservation.customerSource'] = customerSource
        self._params['personalReservation.reserveCheckDate'] = orderExamDate
        self._params['personalReservation.examType'] = examType
        self._params['personalReservation.reportReceivingType'] = '1'
        self._params['personalBaseInfo.email'] = None
        self._params['personalBaseInfo.address'] = None
        self._params['personalReservation.examTimes'] = 1
        # if examNo:
        self._params['personalBaseInfo.examNo'] = examNo  # if examNo is not None else ''
        # if personId:
        self._params['personalReservation.persionId'] = personId  # if personId is not None else ''

        self._params['contractGroupId'] = contractGroupId if contractGroupId is not None else ''
        self._params['itemPackage'] = itemPackage if itemPackage is not None else ''
        self._params['personalReservation.reserveSubarea'] = subarea  # 分区字段

    def addGroup(self, departmentId, groupId, groupName, originalPrice, discountPrice, discountRate, feeType='自费',
                 oldFeeType='自费'):
        # if 'personalItemsStore' not in self._params.keys():
        #     self._params['personalItemsStore'] = []
        _group = {}
        _group['departmentsId'] = departmentId
        _group['id'] = groupId
        _group['name'] = groupName
        _group['price'] = originalPrice
        _group['originalPrice'] = originalPrice
        _group['discountPrice'] = discountPrice
        _group['discountRate'] = discountRate
        _group['priceDifference'] = 0
        if discountRate != 100:
            _group['ifDiscount'] = '是'
        else:
            _group['ifDiscount'] = '否'
        _group['sex'] = ''
        _group['mnemonic'] = ''
        _group['feeType'] = feeType
        _group['oldFeeType'] = oldFeeType
        # self._params['personalItemsStore'].append(_group)
        self._groups.append(_group)

    def getParams(self):
        self._params['personalItemsStore'] = json.dumps(self._groups, ensure_ascii=False)
        return self._params


class Order:
    def __init__(self, orderDict, orderId, examNo, certId, username, sexCode, sex, birth, age, mobile,
                 customerSourceCode,
                 customerSource, examTypeCode, examType, maritalCode, marital, examStatus, orderTime, examTime,
                 subareaCode, subarea, packageId, packageName,orderExamTime):
        self.orderDict = orderDict
        # _groups = []
        # _groupObj = {}
        _order = {
            'orderId': orderId,
            'examNo': examNo,
            'certId': certId,
            'username': username,
            'sexCode': sexCode,
            'sex': sex,
            'birth': birth,
            'age': age,
            'mobile': mobile,
            'customerSourceCode': customerSourceCode,
            'customerSource': customerSource,
            'examTypeCode': examTypeCode,
            'examType': examType,
            'maritalCode': maritalCode,
            'marital': marital,
            'examStatus': examStatus,
            'orderTime': orderTime,
            'examTime': examTime,
            'subareaCode': subareaCode,
            'subarea': subarea,
            'packageId': packageId,
            'packageName': packageName,
            'orderExamTime':orderExamTime
        }

        self.orderDict.update(_order)

    def addGroup(self, departmentId, departmentName, departmentDisplayOrder, groupId, groupName, groupDisplayOrder,
                 clinicalSignificance, originalPrice, discountPrice, discountRate, feeType, costStatus, completeStatus,completeTime):
        _group = {
            'departmentId': departmentId,
            'departmentName': departmentName,
            'departmentDisplayOrder': departmentDisplayOrder,
            'groupId': groupId,
            'groupName': groupName,
            'groupDisplayOrder': groupDisplayOrder,
            'clinicalSignificance': clinicalSignificance,
            'originalPrice': originalPrice,
            'discountPrice': discountPrice,
            'discountRate': discountRate,
            'feeType': feeType,
            'costStatus': costStatus,
            'completeStatus': completeStatus,
            'completeTime': completeTime
        }
        if 'groups' not in self.orderDict.keys():
            self.orderDict['groups'] = []

        self.orderDict['groups'].append(_group)


class Orders:
    def __init__(self):
        self._orders = []
        self._orderObj = {}

    def addOrder(self, orderId, examNo, certId, username, sexCode, sex, birth, age, mobile, customerSourceCode,
                 customerSource, examTypeCode, examType, maritalCode, marital, examStatus, orderTime, examTime,
                 subareaCode, subarea, packageId, packageName,orderExamTime):
        key = str(orderId)
        if key not in self._orderObj.keys():
            _orderDict = {}
            o = Order(_orderDict, orderId, examNo, certId, username, sexCode, sex, birth, age, mobile,
                      customerSourceCode,
                      customerSource, examTypeCode, examType, maritalCode, marital, examStatus, orderTime, examTime,
                      subareaCode, subarea, packageId, packageName,orderExamTime)
            self._orders.append(_orderDict)
            self._orderObj[key] = o

        return self._orderObj[key]

    def toDict(self):
        return self._orders
