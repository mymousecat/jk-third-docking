# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019/8/13
-------------------------------------------------
   Change Activity:
                   2019/8/13:
-------------------------------------------------
"""

from datetime import datetime as dt
from . import db

"""
  本地业务表
"""


class TransLog(db.Model):
    """
      操作日志表
    """
    __tablename__ = 't_lis_translog'
    id = db.Column(db.Integer, autoincrement="auto", primary_key=True)
    barcode_id = db.Column(db.String(100), nullable=False, index=True)
    order_id = db.Column(db.String(100), nullable=False, index=True)

    element_assem_id = db.Column(db.String(100), nullable=False)
    element_assem_name = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(100))
    sex_name = db.Column(db.String(4))
    age = db.Column(db.String(3))

    operator_id = db.Column(db.String(100))
    operator_name = db.Column(db.String(100))

    is_successfull = db.Column(db.Boolean, nullable=False)
    trans_msg = db.Column(db.String(4000))

    sample_date = db.Column(db.Date, nullable=False, index=True)
    trans_date = db.Column(db.Date, nullable=False, default=dt.now())
    trans_time = db.Column(db.DateTime, nullable=False, default=dt.now())


class Duty(db.Model):
    """
    主业务表
    """
    __tablename__ = 't_lis_duty'
    barcode_id = db.Column(db.String(100), primary_key=True)
    element_assem_id = db.Column(db.String(100), primary_key=True)

    order_id = db.Column(db.String(100), nullable=False)

    element_assem_name = db.Column(db.String(100), nullable=False, index=True)

    username = db.Column(db.String(100))
    sex_name = db.Column(db.String(4))
    age = db.Column(db.String(3))

    operator_id = db.Column(db.String(100))
    operator_name = db.Column(db.String(100))

    is_successfull = db.Column(db.Boolean, nullable=False)
    trans_msg = db.Column(db.String(4000))

    sample_date = db.Column(db.Date, nullable=False, index=True)
    trans_date = db.Column(db.Date, nullable=False, default=dt.now())
    trans_time = db.Column(db.DateTime, nullable=False, default=dt.now())


"""
  体检系统数据库表
"""


class LisBarcode(db.Model):
    __tablename__ = 'v_lis_barcode'
    # __bind_key__ = 'jk'
    ID = db.Column(db.String, primary_key=True)
    BARCODE_ID = db.Column(db.String)
    EXAM_NO = db.Column(db.String)
    ORDER_ID = db.Column(db.String)
    USERNAME = db.Column(db.String)
    BIRTHDAY = db.Column(db.String)
    SEX_NAME = db.Column(db.String)
    AGE = db.Column(db.String)
    TELEPHONE = db.Column(db.String)
    ADDRESS = db.Column(db.String)
    SPECIMEN_TYPE_NAME = db.Column(db.String)
    LIS_ELEMENT_ASSEM_ID = db.Column(db.String)
    ELEMENT_ASSEM_NAME = db.Column(db.String)
    ELEMENT_ID = db.Column(db.String)
    ELEMENT_NAME = db.Column(db.String)
    DEPARTMENT_ID = db.Column(db.String)
    REQ_DOCTOR = db.Column(db.String)
    REQ_DATE = db.Column(db.DateTime)


class LisBarcodeDetail(db.Model):
    __tablename__ = 'v_lis_barcode_detail'
    # __bind_key__ = 'jk'
    ELEMENT_ID = db.Column(db.String, primary_key=True)
    ELEMENT_NAME = db.Column(db.String)
    BARCODE_ID = db.Column(db.String)
    ORDER_ID = db.Column(db.String)
    ELEMENT_ASSEM_ID = db.Column(db.String)
    LIS_ELEMENT_ASSEM_ID = db.Column(db.String)
    ELEMENT_ASSEM_NAME = db.Column(db.String)
    LIS_ELEMENT_CODE = db.Column(db.String)


"""
  LIS数据库表
"""

class LisResult(db.Model):
    __tablename__ = 'v_lis_result'
    # __bind_key__ = 'lis'
    # __table_args__ = {'schema': 'portal_lis'}
    ID = db.Column(db.Integer, primary_key=True)
    BARCODE_ID = db.Column(db.String)
    ORDER_ID = db.Column(db.String)
    USERNAME = db.Column(db.String)
    LIS_ELEMENT_ASSEM_ID = db.Column(db.String)
    LIS_ELEMENT_ASSEM_NAME = db.Column(db.String)
    LIS_ELEMENT_ID = db.Column(db.String)
    LIS_ELEMENT_NAME = db.Column(db.String)
    BLOOD_SAMPLE_SHAPE = db.Column(db.String)
    CONTENT_RESULT = db.Column(db.String)
    RESULT_UNIT = db.Column(db.String)
    FERENCE_VALUE = db.Column(db.String)
    FERENCE_LOWER_LIMIT = db.Column(db.String)
    FERENCE_UPPER_LIMIT = db.Column(db.String)
    POSITIVE_SYMBOL = db.Column(db.String)
    CRITICAL_VALUES_SYMBOL = db.Column(db.String)
    SAMPLE_DATE = db.Column(db.DateTime)
    SAMPLE_DOCTOR_ID = db.Column(db.String)
    SAMPLE_DOCTOR = db.Column(db.String)
    OPERATOR_ID = db.Column(db.String)
    OPERATOR_NAME = db.Column(db.String)
    AUDIT_ID = db.Column(db.String)
    AUDIT_NAME = db.Column(db.String)
    AUDIT_DATE = db.Column(db.DateTime)