# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019/2/12
-------------------------------------------------
   Change Activity:
                   2019/2/12:
-------------------------------------------------
"""
from . import db

class MiniProgPackages(db.Model):
    __tablename__ = 'v_miniprog_packages'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    packTypeCode = db.Column(db.String)
    packTypeName = db.Column(db.String)
    sexCode = db.Column(db.String)
    sexName = db.Column(db.String)
    maritalCode = db.Column(db.String)
    maritalName = db.Column(db.String)
    originalPrice = db.Column(db.Float)
    discountPrice = db.Column(db.Float)
    dicountRate = db.Column(db.Float)
    displayOrder = db.Column(db.Integer)
    clinicalSignificance = db.Column(db.String)
    createTime = db.Column(db.DateTime)
    changeTime = db.Column(db.DateTime)


class MiniProgPackageDetails(db.Model):
    __tablename__ = 'v_miniprog_package_detail'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    groupId = db.Column(db.String)
    groupName = db.Column(db.String)
    originalPrice = db.Column(db.Float)
    discountPrice = db.Column(db.Float)
    dicountRate = db.Column(db.Float)
    displayOrder = db.Column(db.Integer)
    clinicalSignificance = db.Column(db.String)
    attention = db.Column(db.String)
    departmentId = db.Column(db.String)
    departmentName = db.Column(db.String)
    packageId = db.Column(db.String)
    itemId = db.Column(db.String)
    itemName = db.Column(db.String)


class MiniProgPackageDetails_():
    def __init__(self):
        self.packageDetails_list = []
        self.packageDetails_dict = {}

    def addPackageDetails(self, skdPackageDetails):
        key = str(skdPackageDetails.groupId)
        if key not in self.packageDetails_dict.keys():
            group = {
                'groupId': skdPackageDetails.groupId,
                'groupName': skdPackageDetails.groupName,
                'originalPrice': skdPackageDetails.originalPrice,
                'discountPrice': skdPackageDetails.discountPrice,
                'dicountRate': skdPackageDetails.dicountRate,
                'displayOrder': skdPackageDetails.displayOrder,
                'clinicalSignificance': skdPackageDetails.clinicalSignificance,
                'attention': skdPackageDetails.attention,
                'departmentId': skdPackageDetails.departmentId,
                'departmentName': skdPackageDetails.departmentName,
                'packageId': skdPackageDetails.packageId,
                'items': []
            }
            self.packageDetails_dict[key] = group
            self.packageDetails_list.append(group)

        items = self.packageDetails_dict[key]['items']
        item = {
            'itemId': skdPackageDetails.itemId,
            'itemName': skdPackageDetails.itemName
        }
        items.append(item)


class MiniProgBaseInfo(db.Model):
    __tablename__ = 't_person'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    exam_no = db.Column(db.String)
    username = db.Column(db.String)
    sex = db.Column(db.String)
    cert_id = db.Column(db.String)
    symbol = db.Column(db.String)


class MiniProgOrderDigest(db.Model):
    __tablename__ = 't_personal_order'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    person_id = db.Column(db.String)
    exam_status = db.Column(db.CHAR(10))
    initial_time = db.Column(db.DateTime)
    symbol = db.Column(db.String)


class MiniProgOrders(db.Model):
    __tablename__ = 'v_miniprog_orders'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    orderId = db.Column(db.Integer)
    examNo = db.Column(db.Integer)
    certId = db.Column(db.String)
    username = db.Column(db.String)
    sexCode = db.Column(db.String)
    sex = db.Column(db.String)
    birth = db.Column(db.String)
    age = db.Column(db.Integer)
    mobile = db.Column(db.String)
    customerSourceCode = db.Column(db.String)
    customerSource = db.Column(db.String)
    examTypeCode = db.Column(db.String)
    examType = db.Column(db.String)
    maritalCode = db.Column(db.String)
    marital = db.Column(db.String)
    examStatus = db.Column(db.String)
    orderTime = db.Column(db.DateTime)
    examTime = db.Column(db.DateTime)
    orderExamTime = db.Column(db.Date)
    subareaCode = db.Column(db.String)
    subarea = db.Column(db.String)
    packageId = db.Column(db.String)
    packageName = db.Column(db.String)
    departmentId = db.Column(db.Integer)
    departmentName = db.Column(db.String)
    departmentDisplayOrder = db.Column(db.Integer)
    groupId = db.Column(db.Integer)
    groupName = db.Column(db.String)
    groupDisplayOrder = db.Column(db.Integer)
    clinicalSignificance = db.Column(db.String)
    originalPrice = db.Column(db.Float)
    discountPrice = db.Column(db.Float)
    discountRate = db.Column(db.Float)
    feeType = db.Column(db.String)
    costStatus = db.Column(db.String)
    completeStatus = db.Column(db.String)
    completeTime = db.Column(db.DateTime)


class MiniProgReportList(db.Model):
    __tablename__ = 'v_miniprog_get_report_list'
    # __bind_key__ = 'skd'
    orderId = db.Column(db.String, primary_key=True)
    examNo = db.Column(db.String)
    certId = db.Column(db.String)
    username = db.Column(db.String)
    birth = db.Column(db.String)
    sexCode = db.Column(db.String)
    sex = db.Column(db.String)
    age = db.Column(db.String)
    companyId = db.Column(db.String)
    companyName = db.Column(db.String)
    examTime = db.Column(db.DateTime)
    examTypeCode = db.Column(db.String)
    examType = db.Column(db.String)
    mainCheckUid = db.Column(db.String)
    mainCheckDoctor = db.Column(db.String)
    mainCheckTime = db.Column(db.DateTime)
    finalCheckUid = db.Column(db.String)
    finalCheckDoctor = db.Column(db.String)
    finalCheckTime = db.Column(db.DateTime)


# 体检报告 models
class MiniProgBasicInfo(db.Model):
    """
       蓝滴体检人员基本信息
    """
    __tablename__ = 'v_miniprog_report_basicinfo'
    # __bind_key__ = 'skd'
    order_id = db.Column(db.String, primary_key=True)
    exam_no = db.Column(db.String)
    cert_id = db.Column(db.String)
    username = db.Column(db.String)
    gender = db.Column(db.String)
    birthday = db.Column(db.String)
    nation = db.Column(db.String)
    telephone = db.Column(db.String)
    address = db.Column(db.String)
    email = db.Column(db.String)
    if_family = db.Column(db.String)
    native_place = db.Column(db.String)
    initial_time = db.Column(db.DateTime)
    change_time = db.Column(db.DateTime)
    org_id = db.Column(db.String)
    org_name = db.Column(db.String)
    contract_id = db.Column(db.String)
    contract_name = db.Column(db.String)
    customer_source = db.Column(db.String)
    departments = db.Column(db.String)
    job_number = db.Column(db.String)
    post = db.Column(db.String)
    exam_type = db.Column(db.String)
    exam_times = db.Column(db.Integer)
    age = db.Column(db.Integer)
    # MARITAL_STATUS
    marital_status = db.Column(db.String)
    arrival_date = db.Column(db.DateTime)
    order_initial_time = db.Column(db.DateTime)
    order_staff = db.Column(db.String)


class MiniProgItemResults(db.Model):
    """
      蓝滴体检项目结果
    """
    __tablename__ = 'v_miniprog_report_items_result'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String)
    department_id = db.Column(db.String)
    department_name = db.Column(db.String)
    deptclass = db.Column(db.String)
    department_display_order = db.Column(db.Integer)
    assem_id = db.Column(db.String)
    assem_name = db.Column(db.String)
    assem_giveup = db.Column(db.String)
    assem_display_order = db.Column(db.Integer)
    assem_type = db.Column(db.String)
    element_id = db.Column(db.String)
    element_name = db.Column(db.String)
    element_display_order = db.Column(db.Integer)
    result_content = db.Column(db.String)
    # MEASUREMENT_UNIT
    measurement_unit = db.Column(db.String)
    # FERENCE_LOWER_LIMIT
    ference_lower_limit = db.Column(db.String)
    # FERENCE_UPPER_LIMIT
    ference_upper_limit = db.Column(db.String)

    result_type = db.Column(db.String)
    # POSITIVE_SYMBOL
    positive_symbol = db.Column(db.String)

    giveup_symbol = db.Column(db.String)


class MiniProgSummaries(db.Model):
    """
      蓝滴体检项目组小结
    """
    __tablename__ = 'v_miniprog_report_summaries'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String)
    department_id = db.Column(db.String)
    element_assem_id = db.Column(db.String)
    operator_id = db.Column(db.String)
    operator_name = db.Column(db.String)
    # ADDITIONAL_OPERATOR_ID
    additional_operator_id = db.Column(db.String)
    # ADDITIONAL_OPERATOR_NAME
    additional_operator_name = db.Column(db.String)

    complete_time = db.Column(db.DateTime)
    # DISEASE_CONTENT
    disease_content = db.Column(db.String)
    # MERGE_WORD
    merge_word = db.Column(db.String)
    # SELFWRITE_SYMBOL
    selfwrite_symbol = db.Column(db.String)


class MiniProgMainCheck(db.Model):
    __tablename__ = 'v_miniprog_report_maincheck'
    # __bind_key__ = 'skd'
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String)
    early_check_uid = db.Column(db.String)
    early_check_name = db.Column(db.String)
    early_check_date = db.Column(db.DateTime)
    main_check_uid = db.Column(db.String)
    main_check_name = db.Column(db.String)
    main_check_date = db.Column(db.DateTime)
    final_check_uid = db.Column(db.String)
    final_check_name = db.Column(db.String)
    final_check_date = db.Column(db.DateTime)
    recommend = db.Column(db.String)
    disease_id = db.Column(db.String)
    merge_word = db.Column(db.String)


"""
  团检
"""


class MiniProgTeamOrder(db.Model):
    __tablename__ = 'v_miniprog_team_cert_id'
    # __bind_key__ = 'skd'
    order_id = db.Column(db.String, primary_key=True)
    cert_id = db.Column(db.String)


class MiniProgTeamOrderDetail(db.Model):
    __tablename__ = 'v_miniprog_team_order'
    # __bind_key__ = 'skd'
    order_id = db.Column(db.String)
    exam_status = db.Column(db.String)
    order_exam_date = db.Column(db.Date)
    age = db.Column(db.String)
    subarea_code = db.Column(db.String)
    subarea = db.Column(db.String)
    exam_no = db.Column(db.String)
    cert_id = db.Column(db.String)
    username = db.Column(db.String)
    sex_code = db.Column(db.String)
    sex = db.Column(db.String)
    birthday = db.Column(db.String)
    telephone = db.Column(db.String)
    company_id = db.Column(db.String)
    company_name = db.Column(db.String)
    exam_begin_date = db.Column(db.Date)
    exam_end_date = db.Column(db.Date)
    department_id = db.Column(db.String)
    department_name = db.Column(db.String)
    department_display_order = db.Column(db.Integer)
    assem_id = db.Column(db.String, primary_key=True)
    assem_name = db.Column(db.String)
    com_display_order = db.Column(db.Integer)
    clinical_significance = db.Column(db.String)
    guidelines_single_prompt = db.Column(db.String)
