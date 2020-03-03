# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019/7/30
-------------------------------------------------
   Change Activity:
                   2019/7/30:
-------------------------------------------------
"""

from .db_op import get_pacs_result_by_order_id
from . import pacs
import logging
from .err import NotFoundException
from .trans import trans_pacs_result

log = logging.getLogger(__name__)


def _getmsg(msg, e):
    if e:
        return '<font color="red"><h2>失败</h2></font><br>{}<br>{}'.format(msg, repr(e))
    else:
        return '<font color="blue"><h2>成功</h2></font><br>{}<br>'.format(msg)


@pacs.route('/<order_id>')
def upload_pacs(order_id):
    msgs = []
    try:
        results = get_pacs_result_by_order_id(order_id)
        if len(results) == 0:
            raise NotFoundException('没有找到预约号为:{}的任何结果记录'.format(order_id))

        for result in results:
            try:
                trans_pacs_result(order_id, result.pacs_assem_id, result.pacs_assem_name, result.report_diagnose,
                                  result.report_result,
                                  result.positive_content, result.report_url, result.reporter, result.audit_doctor,
                                  result.report_date)
                msgs.append(
                    _getmsg('项目组ID:{} 项目组名称:{} 的结果上传成功！'.format(result.pacs_assem_id, result.pacs_assem_name), None))
            except Exception as e:
                log.exception(e)
                msgs.append(
                    _getmsg('接收PACS项目组ID:{} 项目组名称:{}的结果失败'.format(result.pacs_assem_id, result.pacs_assem_name), e))

    except Exception as e:
        log.exception(e)
        msgs.append(_getmsg('接收预约号为:{}的PACS结果失败！'.format(order_id), e))

    log.info('获取到的消息列表:{}'.format(msgs))

    return '<br><hr>'.join(msgs)
