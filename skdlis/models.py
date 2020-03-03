# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""

"""
  本地业务表
"""

from . import db


class TransLog(db.Model):
    """
      操作日志表
    """
    __tablename__ = 't_lis_trans'
    id = db.Column(db.Integer, primary_key=True)
    barcode_id = db.Column(db.String)
    order_id = db.Column(db.String)

    element_assem_id = db.Column(db.String)
    element_assem_name = db.Column(db.String)

    username = db.Column(db.String)
    sex_name = db.Column(db.String)
    age = db.Column(db.String)

    operator_id = db.Column(db.String)
    operator_name = db.Column(db.String)

    is_successfull = db.Column(db.Boolean)
    trans_msg = db.Column(db.String)

    sample_date = db.Column(db.Date)
    trans_date = db.Column(db.Date)
    trans_time = db.Column(db.DateTime)

"""
  LIS数据库表
"""


class LisResult(db.Model):
    __tablename__ = 't_lis_result'
    __bind_key__ = 'lis'
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
