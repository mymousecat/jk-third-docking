# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019/8/13
-------------------------------------------------
   Change Activity:
                   2019/8/13:
-------------------------------------------------
"""

from datetime import timedelta
from datetime import datetime as dt
from sqlalchemy import and_
from . import db
from .models import LisTransLog, LisDuty, LisBarcode, LisResult

"""
操作本地的数据库
"""


def saveLisTransLog(translog):
    try:
        db.session.add(translog)
        duty = db.session.query(LisDuty).get((translog.barcode_id, translog.element_assem_id))
        if duty:
            if not duty.is_successfull:  # 如果上次传输没有成功的话，则更新duty表
                duty.element_assem_id = translog.element_assem_id
                duty.element_assem_name = translog.element_assem_name

                duty.username = translog.username
                duty.sex_name = translog.sex_name
                duty.age = translog.age

                duty.operator_id = translog.operator_id
                duty.operator_name = translog.operator_name

                duty.is_successfull = translog.is_successfull
                duty.trans_msg = translog.trans_msg

                duty.sample_date = translog.sample_date

                duty.trans_date = translog.trans_date
                duty.trans_time = translog.trans_time
                db.session.merge(duty)

        else:
            duty = LisDuty(barcode_id=translog.barcode_id,
                           order_id=translog.order_id,
                           element_assem_id=translog.element_assem_id,
                           element_assem_name=translog.element_assem_name,
                           username=translog.username,
                           sex_name=translog.sex_name,
                           age=translog.age,
                           operator_id=translog.operator_id,
                           operator_name=translog.operator_name,
                           is_successfull=translog.is_successfull,
                           trans_msg=translog.trans_msg,
                           sample_date=translog.sample_date,
                           trans_date=translog.trans_date,
                           trans_time=translog.trans_time
                           )
            db.session.add(duty)
        db.session.commit()

        db.session.refresh(translog)
        db.session.expunge(translog)

    except Exception as e:
        db.session.rollback()
        raise e
    finally:

        db.session.close()


def need_push_mail(barcode_id, element_assem_id):
    """
    查看日志表，以决定是否需要发送邮件
    :param barcode_id:
    :return:
    """
    result = True
    try:
        duty = db.session.query(LisDuty).get((barcode_id, element_assem_id))
        if duty is not None:
            result = not duty.is_successfull
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()

    return result

#
# def clearHistory():
#     """
#     从本地数据库表中，清除60天前的数据
#     :return:
#     """
#     try:
#         twoMonthAgo = (dt.now() + timedelta(days=-60)).date()
#         db.session.query(LisTransLog).filter(LisTransLog.sample_date < twoMonthAgo).delete(synchronize_session=False)
#         db.session.query(LisDuty).filter(LisDuty.sample_date < twoMonthAgo).delete(synchronize_session=False)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e
#     finally:
#         db.session.close()


def query(limit, offset, barcodeId, orderId, onlyErr, beginDate, endDate):
    """
    查询业务
    :param limit: 每页多少行
    :param offset: 第几页
    :param barcodeId:要查询的条码号
    :param orderId:要查询的预约号
    :param onlyErr:是否只查询错误的
    :param beginDate:核收的开始时间
    :param endDate:核收的结束时间
    :return:
    """
    try:
        dutyQuery = db.session.query(LisDuty)
        if barcodeId:
            dutyQuery = dutyQuery.filter(LisDuty.barcode_id == barcodeId)
        if orderId:
            dutyQuery = dutyQuery.filter(LisDuty.order_id == orderId)
        if onlyErr == 'true':
            dutyQuery = dutyQuery.filter(LisDuty.is_successfull == False)
        if beginDate:
            dutyQuery = dutyQuery.filter(LisDuty.sample_date >= beginDate)
        if endDate:
            dutyQuery = dutyQuery.filter(LisDuty.sample_date <= endDate)

        # 使用传输时间的倒序排序
        dutyQuery = dutyQuery.order_by(LisDuty.trans_time.desc())

        page = (offset // limit) + 1

        return dutyQuery.paginate(page, limit, False)

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


"""
  操作体检数据库
"""


def getAssems(barcodeId):
    """
    根据试管号，获取项目列表
    :param barcodeId: 要查询的试管号
    :return: 查询到的列表
    """
    try:
        if barcodeId is not None:
            return db.session.query(LisBarcode).filter(LisBarcode.BARCODE_ID == barcodeId).all()
        else:
            return []
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def getBarcodeByOrderId(order_id):
    """
    根据预约号，获取条码的相关信息
    :param order_id:
    :return:
    """
    try:
        barcodes = db.session.query(LisBarcode).filter(LisBarcode.ORDER_ID == order_id).all()
        return set([str(barcode.BARCODE_ID) for barcode in barcodes])
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


# def getAssemsDetail(barcodeId):
#     """
#     根据试管号，获取小项对照key的字典
#     :param barcodeId:
#     :return:返回字典
#     """
#     try:
#         dict = {}
#         resultList = db.session.query(LisBarcodeDetail).filter(LisBarcodeDetail.BARCODE_ID == barcodeId).all()
#         for result in resultList:
#             key = result.LIS_ELEMENT_CODE
#             dict[key] = result
#         return dict
#     except Exception as e:
#         db.session.rollback()
#         raise e
#     finally:
#         db.session.close()


"""
  操作HIS数据库
"""


def getNextBarcode(ID, barcoceId):
    """
    根据上次保存的自增ID及试管号，获取不同的管号
    :param ID:自增ID
    :param barcoceId: 条码号
    :return:试管号
    """
    try:
        result = None
        if ID is None:
            result = db.session.query(LisResult).order_by(LisResult.ID).first()
        else:
            result = db.session.query(LisResult).filter(
                and_(LisResult.ID > ID, LisResult.BARCODE_ID != barcoceId)).order_by(LisResult.ID).first()
        if result is not None:
            return result.BARCODE_ID
        else:
            return None

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()


def getItems(barcodeId):
    """
    根据试管号，获取项目列表
    :param barcodeId: 要查询的试管号
    :return: 查询到的列表
    """
    try:
        if barcodeId is not None:
            return db.session.query(LisResult).filter(LisResult.BARCODE_ID == barcodeId).order_by(LisResult.ID).all()
        else:
            return []

    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()
