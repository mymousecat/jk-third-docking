# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     reporttemplate
   Description :
   Author :       wdh
   date：          2019/6/12
-------------------------------------------------
   Change Activity:
                   2019/6/12:
-------------------------------------------------
"""


class AdviceInfos(object):
    def __init__(self, adviceInfoDict):
        self.adviceInfo = adviceInfoDict

    def addAdvise(self, diseaseName, diseaseAdvice, diseaseId=None, **others):
        """

        :param diseaseName:       疾病名称
        :param diseaseAdvice:     疾病建议
        :param diseaseId:         疾病id
        :param others:
        :return:
        """
        _advise = {
            'diseaseName': diseaseName,
            'diseaseAdvice': diseaseAdvice,
            'diseaseId': diseaseId,
            'others': {}
        }
        _advise['others'].update(others)

        if 'advice' not in self.adviceInfo.keys():
            self.adviceInfo['advice'] = []
        self.adviceInfo['advice'].append(_advise)
        return self


class Summary(object):

    def __init__(self, departmentOrGroupDict, summary, desc=None, operatorId=None, operatorName=None, reportId=None,
                 reportName=None, auditId=None, auditName=None, examTime=None, **others):
        self.departmentOrGroup = departmentOrGroupDict
        if 'summaries' not in self.departmentOrGroup.keys():
            self.departmentOrGroup['summaries'] = []
        self.summary = {
            'summary': summary,
            'desc': desc,
            'operatorId': operatorId,
            'operatorName': operatorName,
            'reportId': reportId,
            'reportName': reportName,
            'auditId': auditId,
            'auditName': auditName,
            'examTime': examTime,
            'others': {}
        }
        self.summary['others'].update(others)
        self.departmentOrGroup['summaries'].append(self.summary)


class Item(object):

    def __init__(self, groupDict, itemCode, itemName, itemResult, itemType=None, itemUnit=None, flag=None, itemRef=None,
                 **others):
        self.group = groupDict
        if 'items' not in self.group.keys():
            self.group['items'] = []
        self.item = {
            'itemCode': itemCode,
            'itemName': itemName,
            'itemResult': itemResult,
            'itemType': itemType,
            'itemUnit': itemUnit,
            'flag': flag,
            'itemRef': itemRef,
            'others': {}
        }
        self.item['others'].update(others)
        self.group['items'].append(self.item)


class Group(object):

    def __init__(self, departmentDict, groupCode, groupName, groupType=None, displayOrder=None, specimenProp=None,
                 **others):
        self.department = departmentDict
        if 'groups' not in self.department.keys():
            self.department['groups'] = []
        self.group = {
            'groupCode': groupCode,
            'groupName': groupName,
            'groupType': groupType,
            'displayOrder': displayOrder,
            'specimenProp': specimenProp,
            'others': {}
        }
        self.group['others'].update(others)
        self.department['groups'].append(self.group)
        self.items = {}
        self.summaries = {}

    def addItem(self, itemCode, itemName, itemResult, itemType=None, itemUnit=None, flag=None, itemRef=None, **others):
        """
        新增小项
        :param itemCode:    项目代码
        :param itemName:    项目名称
        :param itemResult:  项目结果
        :param itemType:    项目类型
        :param itemUnit:    项目单位
        :param flag:        异常标示
        :param itemRef:     参考范围
        :param others:
        :return:
        """
        key = str(itemCode)
        if key in self.items.keys():
            return self.items[key]
        else:
            item = Item(self.group, itemCode, itemName, itemResult, itemType, itemUnit, flag, itemRef, **others)
            self.items[key] = item
            return item

    def addSummary(self, summary, desc=None, operatorId=None, operatorName=None, reportId=None,
                   reportName=None, auditId=None, auditName=None, examTime=None, **others):
        """
        新增结论
        :param summary:          结论
        :param desc:             结论描述
        :param operatorId:       操作医生
        :param operatorName:     操作医生姓名
        :param reportId:         报告医生
        :param reportName:       报告医生姓名
        :param auditId:          审核医生
        :param auditName:        审核医生姓名
        :param examTime:         检查时间
        :param others:
        :return:
        """
        key = str(summary)

        if key not in self.summaries.keys():
            summary = Summary(self.group, summary, desc, operatorId, operatorName, reportId,
                              reportName, auditId, auditName, examTime, **others)
            self.summaries[key] = summary
        return self.summaries[key]


class Department(object):

    def __init__(self, examInfosDict, departmentCode, departmentName, departmentType=None, desc=None, displayOrder=None,
                 **others):
        self.examInfos = examInfosDict
        self.department = {
            'departmentCode': departmentCode,
            'departmentName': departmentName,
            'departmentType': departmentType,
            'desc': desc,
            'displayOrder': displayOrder,
            'others': {}
        }
        self.department['others'].update(others)

        self.examInfos.append(self.department)

        self.groups = {}

        self.summaries = {}

    def addGroup(self, groupCode, groupName, groupType=None, displayOrder=None, specimenProp=None, **others):
        """
        增加项目组（大项）
        :param groupCode:       大项代码
        :param groupName:       大项名称
        :param groupType:       大项类型
        :param displayOrder:    大项显示顺序
        :param specimenProp:    标本性状
        :param others:
        :return:
        """
        key = str(groupCode)
        if groupName:
            if key not in self.groups.keys():
                group = Group(self.department, groupCode, groupName, groupType, displayOrder, specimenProp, **others)
                self.groups[key] = group
            return self.groups[key]
        else:
            if key not in self.groups.keys():
                return None
            return self.groups[key]

    def addSummary(self, summary, desc=None, operatorId=None, operatorName=None, reportId=None,
                   reportName=None, auditId=None, auditName=None, examTime=None, **others):
        """
        新增结论
        :param summary:          结论
        :param desc:             结论描述
        :param operatorId:       操作医生
        :param operatorName:     操作医生姓名
        :param reportId:         报告医生
        :param reportName:       报告医生姓名
        :param auditId:          审核医生
        :param auditName:        审核医生姓名
        :param examTime:         检查时间
        :param others:
        :return:
        """
        key = str(summary)
        if key not in self.summaries.keys():
            summary = Summary(self.group, summary, desc, operatorId, operatorName, reportId,
                              reportName, auditId, auditName, examTime, **others)
            self.summaries[key] = summary
        return self.summaries[key]


class ExamInfos(object):

    def __init__(self, examInfosDict):
        self.examInfos = examInfosDict
        self.departments = {}

    def addDepartment(self, departmentCode, departmentName, departmentType=None, desc=None, displayOrder=None,
                      **others):
        """

        :param departmentCode:  科室代码
        :param departmentName:  科室名称
        :param departmentType:  科室类型
        :param desc:            科室描述
        :param displayOrder:    科室显示顺序
        :param others:
        :return:
        """
        key = str(departmentCode)
        if departmentName:
            if key not in self.departments.keys():
                department = Department(self.examInfos, departmentCode, departmentName, departmentType, desc,
                                        displayOrder,
                                        **others)
                self.departments[key] = department
            return self.departments[key]
        else:
            if key not in self.departments.keys():
                return None
            return self.departments[key]


class ExamReportTemplate(object):

    def __init__(self):
        self.examReport = {}

    def buildCenterInfo(self, centerId, centerName, chain=None, chainName=None, **others):
        """
        中心信息
        :param centerId:                         #中心id 不能为空
        :param centerName:                       #体检中心名称 不能为空
        :param chian:                            #连锁编码 如没有，可为空
        :param chainName:                        #连锁名称 如没有，可为空
        :param others:
        :return:
        """
        CENTER_INFO = 'centerInfo'

        _centerInfo = {
            'centerId': centerId,
            'centerName': centerName,
            'chain': chain,
            'chainName': chainName,
            'others': {}
        }
        _centerInfo['others'].update(others)

        if CENTER_INFO in self.examReport.keys():
            self.examReport.pop(CENTER_INFO)

        self.examReport[CENTER_INFO] = _centerInfo

        return self

    def buildBasicInfo(self, persionId, username, gender, birth=None, nation=None, certId=None, created=None,
                       changed=None, **others):
        """
        个人基本信息
        :param persionId:                   # 人员id,不能为空
        :param username:                    # 姓名,不能为空
        :param gender:                      # 性别，不能为空
        :param birth:                       # 出身日期，可为空
        :param nation:                      # 民族,可为空
        :param certId:                      # 身份证号，可为空
        :param created:                     # 信息创建时间,可为空
        :param changed:                     # 信息修改时间，可为空
        :param others:
        :return:
        """
        BASIC_INFO = 'basicInfo'

        _basicInfo = {
            'personId': persionId,
            'username': username,
            'gender': gender,
            'birth': birth,
            'nation': nation,
            'certId': certId,
            'created': created,
            'changed': changed,
            'others': {}
        }
        _basicInfo['others'].update(others)

        if BASIC_INFO in self.examReport.keys():
            self.examReport.pop(BASIC_INFO)

        self.examReport[BASIC_INFO] = _basicInfo
        return self

    def buildContactInfo(self, mobile, currentAddress=None, nativePlace=None, **others):
        """
        通讯信息
        :param mobile:              #手机号，不能为空
        :param currentAddress:      #现居住地
        :param nativePlace:         #籍贯
        :param others:
        :return:
        """
        CONTRACT_INFO = 'contactInfo'

        _contactInfo = {
            'mobile': mobile,
            'currentAddress': currentAddress,
            'nativePlace': nativePlace,
            'others': {}
        }
        _contactInfo['others'].update(others)

        if CONTRACT_INFO in self.examReport.keys():
            self.examReport.pop(CONTRACT_INFO)

        self.examReport[CONTRACT_INFO] = _contactInfo
        return self

    def buildCompanyInfo(self, companyName, companyId=None, contractId=None, contractName=None, companyAddr=None,
                         contact=None, telephone=None, department=None, post=None, workNo=None, **others):
        """
        公司信息
        :param companyName:             #公司名称
        :param companyId:               #公司标识id
        :param contractId:              #合同标识id
        :param contractName:            #合同名称
        :param companyAddr:             #公司地址
        :param contact:                 #公司联系人
        :param telephone:               #联系人电话
        :param department:              #所在部门
        :param post:                    #职务
        :param workNo:                  #工号
        :param others:
        :return:
        """
        COMPANY_INFO = 'companyInfo'

        _companyInfo = {
            'companyName': companyName,
            'companyId': companyId,
            'contractId': contractId,
            'contractName': contractName,
            'companyAddr': companyAddr,
            'contact': contact,
            'telephone': telephone,
            'department': department,
            'post': post,
            'workNo': workNo,
            'others': {}
        }
        _companyInfo['others'].update(others)

        if COMPANY_INFO in self.examReport.keys():
            self.examReport.pop(COMPANY_INFO)

        self.examReport[COMPANY_INFO] = _companyInfo

        return self

    def buildOrderInfo(self, orderId, valid, opId=None, opName=None, age=None, examDate=None, examType=None,
                       orderStaff=None, orderTime=None, orderWay=None, **others):
        """
        预约信息
        :param orderId:       预约号
        :param valid:         是否有效
        :param opId:          操作者id
        :param opName:        操作者姓名
        :param age:           年龄
        :param examDate:      检查日期
        :param examType:      体检类型
        :param orderStaff:    接单人姓名
        :param orderTime:     接单时间
        :param orderWay:      下单类型
        :param others:
        :return:
        """
        ORDER_INFO = 'orderInfo'

        _orderInfo = {
            'orderId': orderId,
            'valid': valid,
            'opId': opId,
            'opName': opName,
            'age': age,
            'examDate': examDate,
            'examType': examType,
            'orderStaff': orderStaff,
            'orderTime': orderTime,
            'orderWay': orderWay,
            'others': {}
        }
        _orderInfo['others'].update(others)

        if ORDER_INFO in self.examReport.keys():
            self.examReport.pop(ORDER_INFO)

        self.examReport[ORDER_INFO] = _orderInfo
        return self

    def createAdviceInfos(self, mainCheckDoctorId=None, mainCheckDoctorName=None, mainCheckTime=None,
                          finalCheckDoctorId=None, finalCheckDoctorName=None, finalCheckTime=None, **others):
        """
        创建AdviceInfos类
        :param mainCheckDoctorId:                        主检医生id
        :param mainCheckDoctorName:                      主检医生姓名
        :param mainCheckTime:                            主检时间
        :param finalCheckDoctorId:                       终检医生id
        :param finalCheckDoctorName:                     终检医生姓名
        :param finalCheckTime                            终检时间
        :return:
        """
        ADVICE_INFOS = 'adviceInfos'

        if ADVICE_INFOS not in self.examReport.keys():
            _adviceInfos = {
                'mainCheckDoctorId': mainCheckDoctorId,
                'mainCheckDoctorName': mainCheckDoctorName,
                'mainCheckTime': mainCheckTime,
                'finalCheckDoctorId': finalCheckDoctorId,
                'finalCheckDoctorName': finalCheckDoctorName,
                'finalCheckTime': finalCheckTime,
                'others': {}
            }
            _adviceInfos['others'].update(others)
            self.examReport[ADVICE_INFOS] = _adviceInfos

        return AdviceInfos(self.examReport[ADVICE_INFOS])

    def createExamInfos(self):
        """
        创建检查类
        :return:
        """
        EXAM_INFOS = 'examInfos'

        if EXAM_INFOS not in self.examReport.keys():
            self.examReport[EXAM_INFOS] = []
        return ExamInfos(self.examReport[EXAM_INFOS])

    # def toJson(self, indent=None):
    #     return _toJson(self.examReport, indent)
