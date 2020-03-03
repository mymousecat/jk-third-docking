# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task
   Description :
   Author :       wdh
   date：          2019/8/29
-------------------------------------------------
   Change Activity:
                   2019/8/29:
-------------------------------------------------
"""
import logging
from .transbyorderid import trans_skdlis_by_order_id
from .db_op import add_lis_trans, get_next_id
from .params import CurPosParams
from .err import TjAssemResultsException, Success
from .models import TransLog
from datetime import datetime

log = logging.getLogger('skdlis_trans')


def _add_lis_trans(msg):
    try:
        success = None
        m = None
        if isinstance(msg, TjAssemResultsException):
            success = False
            m = repr(msg)
        elif isinstance(msg, Success):
            success = True
            m = '传输成功'

        translog = TransLog()
        translog.order_id = msg.order_id
        translog.username = msg.username
        translog.age = msg.age
        translog.sex_name = msg.sex_name
        translog.element_assem_id = msg.assem_id
        translog.element_assem_name = msg.assem_name
        translog.is_successfull = success
        translog.trans_msg = m

        translog.sample_date = datetime.now().date()
        translog.trans_date = datetime.now().date()
        translog.trans_time = datetime.now()
        add_lis_trans(translog)

    except Exception as e:
        log.error('写入传输日志时发生错误')
        log.exception(e)


def _log_msg(order_id, msgs):
    for msg in msgs:
        if isinstance(msg, TjAssemResultsException):
            log.error('预约号:{} 项目组id:{} 项目组名称:{} 的检验结果上传失败！原因:{}'.format(msg.order_id, msg.assem_id, msg.assem_name,
                                                                        repr(msg)))
            # 写入传输日志
            _add_lis_trans(msg)

        elif isinstance(msg, Success):
            log.info('预约号:{} 项目组id:{} 项目组名称:{} 的检验结果上传成功！'.format(msg.order_id, msg.assem_id, msg.assem_name))
            # 写入传输日志
            _add_lis_trans(msg)

        else:
            log.error('预约号为:{}的检验结果上传失败，原因:{}'.format(order_id, repr(msg)))


def autoTransSkdLis():
    try:
        log.info('开始从当前的配置文件中，获取id...')
        param = CurPosParams()
        cur_id = param.get()
        cur_id = 0 if cur_id is None else cur_id
        log.info('获取到当前的id:{}'.format(cur_id))
        log.info('开始从lis中获取大于id:{}的结果记录...'.format(cur_id))
        lis_result = get_next_id(cur_id)
        if lis_result is None:
            log.info('没有在lis中，获取id大于{}的记录记录，程序将退出...'.format(cur_id))
            return
        msgs = trans_skdlis_by_order_id(lis_result.ORDER_ID, cur_id)
        _log_msg(lis_result.ORDER_ID, msgs)
    except Exception as e:
        log.error(e)
        log.exception(e)
    finally:
        log.info('***************************************************************')
