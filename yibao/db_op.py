# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019/7/17
-------------------------------------------------
   Change Activity:
                   2019/7/17:
-------------------------------------------------
"""

from .models import BasicInfo, Recheck, Summary, ElementResult, ExamMedia, YibaoTransLog
from . import db
from sqlalchemy import and_


def get_basicinfo(order_id):
    """
    获取体检人员基本信息
    :param order_id:
    :return:
    """
    try:
        return db.session.query(BasicInfo).get(order_id)
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_recheck(order_id):
    """
    获取主检信息
    :param order_id:
    :return:
    """
    try:
        return db.session.query(Recheck).filter(Recheck.order_id == order_id).all()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_summary(order_id):
    """
    获取项目组结论
    :param order_id:
    :return:
    """
    try:
        summaries = db.session.query(Summary).filter(Summary.order_id == order_id).all()
        summary_dict = {}
        for summary in summaries:
            key = str(summary.element_assem_id)
            if key not in summary_dict.keys():
                summary_dict[key] = []
            summary_dict[key].append(summary)
        return summary_dict

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_element_result(order_id):
    """
    获取项目结果
    :param order_id:
    :return:
    """
    try:
        return db.session.query(ElementResult).filter(ElementResult.order_id == order_id).all()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_image_dict(order_id):
    """
    获取图像列表
    :param order_id:
    :return:
    """
    try:
        image_list = db.session.query(ExamMedia).filter(
            and_(ExamMedia.order_id == order_id, ExamMedia.is_print_in_report == '是')).all()
        images_dict = {}
        for image in image_list:
            key = str(image.element_assem_id)
            if key not in images_dict.keys():
                images_dict[key] = []
            images_dict[key].append(image)
        return len(image_list), images_dict
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_yibao_trans_id(cur_id):
    """
    从医保传输表中，通过当前的id，获取下一个id
    :param cur_id:
    :return:
    """
    try:
        query = db.session.query(YibaoTransLog)
        if cur_id is not None:
            query = query.filter(YibaoTransLog.id > cur_id)
        return query.order_by(YibaoTransLog.id).first()

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def save_yibao_trans(trans):
    """
    更新传输日志
    :param trans:
    :return:
    """
    try:
        db.session.merge(trans)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()
