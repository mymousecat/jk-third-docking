# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019/7/23
-------------------------------------------------
   Change Activity:
                   2019/7/23:
-------------------------------------------------
"""
from . import db,getSession
from .models import PacsReg, PacsResult, AssemSub, PacsTransLog
from sqlalchemy import and_
from datetime import datetime


def get_next_pacs_result_id(cur_id):
    session = getSession()
    try:
        query = session.query(PacsResult)
        if cur_id is not None:
            query = query.filter(PacsResult.id > cur_id)
        return query.order_by(PacsResult.id).first()
    finally:
        session.close()


def get_next_pacs_reg_id(cur_id):
    session = getSession()
    try:
        query = session.query(PacsReg)
        if cur_id is not None:
            query = query.filter(PacsReg.id > cur_id)
        return query.order_by(PacsReg.id).first()
    finally:
        session.close()


def get_assem_by_id(assem_id):
    session = getSession()
    try:
        return session.query(AssemSub).filter(AssemSub.id == assem_id).all()
    finally:
        session.close()


def get_assem_by_map(DEPARTMENTS, map_code):
    session = getSession()
    try:
        return session.query(AssemSub).filter(
            and_(AssemSub.department_id.in_(DEPARTMENTS), AssemSub.external_sys_control_code == map_code)).all()
    finally:
        session.close()


def get_pacs_result_by_order_id(order_id):
    session = getSession()
    try:
        return session.query(PacsResult).filter(PacsResult.order_id == order_id).order_by(PacsResult.id).all()
    finally:
        session.close()


def add_pacs_log(order_id, pacs_assem_id, pacs_assem_name, log_type, msg):
    session = getSession()
    try:
        log = session.query(PacsTransLog).filter(
            and_(PacsTransLog.order_id == order_id, PacsTransLog.pacs_assem_id == pacs_assem_id,
                 PacsTransLog.log_type == log_type)).first()
        if log is None:
            log = PacsTransLog()
            log.order_id = order_id
            log.pacs_assem_id = pacs_assem_id
            log.pacs_assem_name = pacs_assem_name
            log.log_type = log_type
            log.msg = msg
        else:
            log.msg = msg

        log.trans_time = datetime.now()

        session.merge(log)
        session.commit()

    finally:
        session.close()
