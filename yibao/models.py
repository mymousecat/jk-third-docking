# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019/7/17
-------------------------------------------------
   Change Activity:
                   2019/7/17:
-------------------------------------------------
"""

from . import db


class BasicInfo(db.Model):
    """
    体检中的基本信息
    """
    __tablename__ = 'v_yibao_basicinfo'
    order_id = db.Column(db.String, primary_key=True)
    sex = db.Column(db.String)
    username = db.Column(db.String)
    cert_id = db.Column(db.String)
    age = db.Column(db.String)
    telephone = db.Column(db.String)
    job_number = db.Column(db.String)
    arrival_date = db.Column(db.String)
    main_check_doctor = db.Column(db.String)


class Recheck(db.Model):
    """
    主检建议
    """
    __tablename__ = 'v_yibao_recheck'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String)
    merge_word = db.Column(db.String)
    recommend = db.Column(db.String)


class Summary(db.Model):
    """
    项目组结论
    """
    __tablename__ = 'v_yibao_summary'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String)
    element_assem_id = db.Column(db.String)
    merge_word = db.Column(db.String)
    # SELFWRITE_SYMBOL
    selfwrite_symbol = db.Column(db.String)
    map_code = db.Column(db.String)


class ElementResult(db.Model):
    """
    项目结果信息
    """
    __tablename__ = 'v_yibao_itemresult'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String)
    department_id = db.Column(db.String)
    department_name = db.Column(db.String)
    assem_id = db.Column(db.String)
    assem_name = db.Column(db.String)
    addop_name = db.Column(db.String)
    doc_name = db.Column(db.String)
    element_id = db.Column(db.String)
    element_name = db.Column(db.String)
    map_code = db.Column(db.String)
    result_type = db.Column(db.String)
    result_content = db.Column(db.String)
    unit = db.Column(db.String)
    low = db.Column(db.String)
    upper = db.Column(db.String)
    positive = db.Column(db.String)
    giveup_symbol = db.Column(db.String)
    default_value = db.Column(db.String)


class ExamMedia(db.Model):
    """
    图像信息
    """
    __tablename__ = 't_exam_media'
    file_id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String)
    department_id = db.Column(db.String)
    content_type = db.Column(db.String)
    element_assem_id = db.Column(db.String)
    file_ext = db.Column(db.String)
    is_print_in_report = db.Column(db.String)
    image_date = db.Column(db.Date)


class YibaoTransLog(db.Model):
    """
      医保上传记录表
    """
    __tablename__ ='t_yibao_trans_log'
    id = db.Column(db.Integer,primary_key=True)
    order_id = db.Column(db.String)
    trans_time = db.Column(db.DateTime)
    success = db.Column(db.String)
    msg = db.Column(db.String)
    created = db.Column(db.String)

