# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""
import logging
from .params import CurPosParams
from .db_op import get_yibao_trans_id, save_yibao_trans
from .err import NotFoundNewTransLogException, XMLException, NotFoundException, InValidException, InvokeException
from .upload import upload
import datetime

log = logging.getLogger(__name__)


def yibaoTrans():
    tranLog = None
    next_id = None
    curPos = CurPosParams()
    try:
        log.log('从当前的配置文件中获取ID...')
        id = curPos.get()
        log.log('获取当前的id:{}'.format(id))
        log.log('从传输日志表中获取当前的传输日志对象...')
        tranLog = get_yibao_trans_id(id)
        if tranLog is None:
            raise NotFoundNewTransLogException('没有找到新的传输日志对象，程序将退出...')
        next_id = tranLog.id
        upload(tranLog.order_id)

        curPos.save(next_id)

        tranLog.success = '成功'
        tranLog.trans_time = datetime.datetime.now()
        save_yibao_trans(tranLog)

        log.log('预约号为:{}的报告上传成功!'.format(tranLog.order_id))

    except NotFoundNewTransLogException as e:
        log.exception(repr(e))

    except (XMLException, NotFoundException, InValidException, InvokeException) as e:
        curPos.save(next_id)

        tranLog.success = '错误'
        tranLog.trans_time = datetime.datetime.now()
        tranLog.msg = repr(e)
        save_yibao_trans(tranLog)

        log.error('上传体检报告失败!')
        log.exception(e)
