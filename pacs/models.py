# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019/7/22
-------------------------------------------------
   Change Activity:
                   2019/7/22:
-------------------------------------------------
"""

from . import db


class PacsResult(db.Model):
    """
      PACS结果表
    """
    __tablename__ = 'T_PACS_RESULT'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String)
    pacs_assem_id = db.Column(db.String)
    pacs_assem_name = db.Column(db.String)
    username = db.Column(db.String)
    report_diagnose = db.Column(db.String)
    report_result = db.Column(db.String)
    positive_content = db.Column(db.String)
    report_url = db.Column(db.String)
    reporter_id = db.Column(db.String)
    reporter = db.Column(db.String)
    report_date = db.Column(db.DateTime)
    audit_doctor_id = db.Column(db.String)
    audit_doctor = db.Column(db.String)
    audit_date = db.Column(db.DateTime)


class PacsReg(db.Model):
    """
    PACS登记表
    """
    __tablename__ = 'T_PACS_REG'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String)
    pacs_assem_id = db.Column(db.String)
    pacs_assem_name = db.Column(db.String)
    modality = db.Column(db.String)
    op_type = db.Column(db.String)
    op_name = db.Column(db.String)


class AssemSub(db.Model):
    """
    项目组
    """
    __tablename__ = 't_element_assem_sub'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.String)
    name = db.Column(db.String)
    default_summary = db.Column(db.String)
    external_sys_control_code = db.Column(db.String)
    symbol = db.Column(db.String)


# create table T_PACS_TRANS_LOG
# (
#    ID int not null auto_increment,
#    ORDER_ID             int not null,
#    PACS_ASSEM_ID        varchar(50) not null,
#    PACS_ASSEM_NAME      varchar(100) not null,
#    LOG_TYPE             varchar(20),
#    MSG                  varchar(4000),
#    TRANS_TIME           datetime
# );

class PacsTransLog(db.Model):
    """
    放射传输日志
    """
    __tablename__ = 't_pacs_trans_log'
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.String)
    pacs_assem_id = db.Column(db.String)
    pacs_assem_name = db.Column(db.String)
    log_type = db.Column(db.String)
    msg = db.Column(db.String)
    trans_time = db.Column(db.DateTime)

