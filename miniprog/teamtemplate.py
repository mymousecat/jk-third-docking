# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     teamtemplate
   Description :
   Author :       wdh
   date：          2019/6/13
-------------------------------------------------
   Change Activity:
                   2019/6/13:
-------------------------------------------------
"""

"""
  团检信息模板
"""


class TeamOrderDetailsTemplate:

    def __init__(self):
        self.teamOrderDtails = {
            'groups': []
        }

    def addBasicInfo(self, orderId, examStatus, orderExamDate, subareaCode,age ,subarea, examNo, certId, username, sexCode,
                     sex, birth, telephone, companyId, companyName, examBeginDate, examEndDate):
        self.teamOrderDtails['orderId'] = orderId
        self.teamOrderDtails['examStatus'] = examStatus.strip() if examStatus is not None else None
        self.teamOrderDtails['orderExamDate'] = orderExamDate
        self.teamOrderDtails['age'] = age
        self.teamOrderDtails['subarea'] = subarea
        self.teamOrderDtails['examNo'] = examNo
        self.teamOrderDtails['certId'] = certId
        self.teamOrderDtails['username'] = username
        self.teamOrderDtails['sexCode'] = sexCode
        self.teamOrderDtails['sex'] = sex
        self.teamOrderDtails['birth'] = birth
        self.teamOrderDtails['mobile'] = telephone
        self.teamOrderDtails['companyId'] = companyId
        self.teamOrderDtails['companyName'] = companyName
        self.teamOrderDtails['examBeginDate'] = examBeginDate
        self.teamOrderDtails['examEndDate'] = examEndDate

    def addGroup(self, departmentId, departmentName, departmentDisplayOrder, groupId, groupName, groupDisplayOrder,
                 clinicalSignificance, attention):
        _group = {
            'departmentId': departmentId,
            'departmentName': departmentName,
            'departmentDisplayOrder': departmentDisplayOrder,
            'groupId': groupId,
            'groupName': groupName,
            'groupDisplayOrder': groupDisplayOrder,
            'clinicalSignificance': clinicalSignificance,
            'attention': attention
        }
        self.teamOrderDtails['groups'].append(_group)
