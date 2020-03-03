# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""
from . import db
from .models import LisResult


def get_next_id(cur_id):
    """
    根据当前的id，获取比id大的结果记录
    :param cur_id:
    :return:
    """
    try:
        query = db.session.query(LisResult)
        if cur_id is not None:
            query = query.filter(LisResult.ID > cur_id)
        return query.order_by(LisResult.ID).first()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def get_lis_result(order_id):
    """
    根据预约号，在lis中查询所有的结果
    :param order_id:
    :return:
    """
    try:
        return db.session.query(LisResult).filter(LisResult.ORDER_ID == order_id).order_by(LisResult.ID).all()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def add_lis_trans(lis_trans):
    """
    增加lis操作记录
    :param lis_trans:
    :return:
    """
    try:
        db.session.add(lis_trans)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()
