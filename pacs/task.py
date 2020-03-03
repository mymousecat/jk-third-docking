# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task
   Description :
   Author :       wdh
   date：          2019/9/6
-------------------------------------------------
   Change Activity:
                   2019/9/6:
-------------------------------------------------
"""

import logging
from .params import PacsRegParams, PacsResultParams
from .db_op import get_next_pacs_reg_id, add_pacs_log, get_next_pacs_result_id
from .trans import trans_pacs_reg, trans_pacs_result
from jktj.tjexception import TJException
from .err import InvalidOpTypeException, InvalidDialogException, InvalidMultiException, NotFoundException

log = logging.getLogger(__name__)


def _add_log(pacs_reg, pacs_result, log_type, msg):
    try:
        order_id = None
        pacs_assem_id = None
        pacs_assem_name = None
        if pacs_reg:
            order_id = pacs_reg.order_id
            pacs_assem_id = pacs_reg.pacs_assem_id
            pacs_assem_name = pacs_reg.pacs_assem_name
        if pacs_result:
            order_id = pacs_result.order_id
            pacs_assem_id = pacs_result.pacs_assem_id
            pacs_assem_name = pacs_result.pacs_assem_name

        add_pacs_log(order_id, pacs_assem_id, pacs_assem_name, log_type, msg)

    except Exception as e:
        log.error('写入日志失败')
        log.exception(e)


def autoTransPacsResult():
    """自动上传pacs结果"""
    param = PacsResultParams()
    next_id = None
    pacs_result = None
    try:
        log.info('从当前的pacs结果配置文件中获取ID...')
        cur_id = param.get()
        cur_id = cur_id if cur_id is not None else 0
        next_id = cur_id + 1
        log.info('获取配置文件ID为:{}'.format(cur_id))
        log.info('开始使用ID:{}，从PACS结果信息表中，获取PACS结果...'.format(cur_id))
        pacs_result = get_next_pacs_result_id(cur_id)
        if pacs_result is None:
            log.info('没有找到比id:{}大的项目组结果记录,程序将返回...'.format(cur_id))
            return

        trans_pacs_result(order_id=pacs_result.order_id,
                          pacs_assem_id=pacs_result.pacs_assem_id,
                          pacs_assem_name=pacs_result.pacs_assem_name,
                          report_diagnose=pacs_result.report_diagnose,
                          report_result=pacs_result.report_result,
                          positive_content=pacs_result.positive_content,
                          report_url=pacs_result.report_url,
                          reporter=pacs_result.reporter,
                          audit_doctor=pacs_result.audit_doctor,
                          report_date=pacs_result.audit_date
                          )

        param.save(next_id)
        log.info(
            '预约号:{} 项目组id:{} 项目名称:{} 登记成功!'.format(pacs_result.order_id, pacs_result.pacs_assem_id,
                                                   pacs_result.pacs_assem_name))

        _add_log(None, pacs_result, '上传PACS结果', '上传成功')

    except (TJException, InvalidDialogException, InvalidMultiException, NotFoundException) as e:
        param.save(next_id)
        _add_log(None, pacs_result, '上传PACS结果', '上传PACS结果失败!{}'.format(repr(e)))
        log.error(
            '预约号:{} 项目组id:{} 项目名称:{} 登记失败!'.format(pacs_result.order_id, pacs_result.pacs_assem_id,
                                                   pacs_result.pacs_assem_name))
        log.exception(e)

    except Exception as e:
        log.error('项目组上传结果失败')
        log.exception(e)


def autoTransPacsReg():
    """自动上传pacs登记"""
    param = PacsRegParams()
    next_id = None
    pacs_reg = None
    try:
        log.info('从当前的[登记]配置文件中获取ID...')
        cur_id = param.get()
        cur_id = cur_id if cur_id is not None else 0
        next_id = cur_id + 1
        log.info('获取配置文件ID为:{}'.format(cur_id))
        log.info('开始使用ID:{}，从登记信息表中，获取登记信息...'.format(cur_id))
        pacs_reg = get_next_pacs_reg_id(cur_id)
        if pacs_reg is None:
            log.info('没有找到比id:{}大的项目组登记记录,程序将返回...'.format(cur_id))
            return

        trans_pacs_reg(pacs_reg.order_id, pacs_reg.pacs_assem_id, pacs_reg.op_type, pacs_reg.op_name)
        param.save(next_id)
        log.info(
            '预约号:{} 项目组id:{} 项目名称:{} 登记成功!'.format(pacs_reg.order_id, pacs_reg.pacs_assem_id, pacs_reg.pacs_assem_name))

        _add_log(pacs_reg, None, '登记', '登记成功')

    except (TJException, InvalidOpTypeException,NotFoundException) as e:
        param.save(next_id)
        _add_log(pacs_reg, None, '登记', '登记失败!{}'.format(repr(e)))
        log.error(
            '预约号:{} 项目组id:{} 项目名称:{} 登记失败!'.format(pacs_reg.order_id, pacs_reg.pacs_assem_id, pacs_reg.pacs_assem_name))
        log.exception(e)


    except Exception as e:
        log.error('项目组登记失败')
        log.exception(e)
