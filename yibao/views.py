# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019/7/19
-------------------------------------------------
   Change Activity:
                   2019/7/19:
-------------------------------------------------
"""

from . import yibao
from .upload import upload

import logging

log = logging.getLogger(__name__)

@yibao.route('/<order_id>')
def up_exam(order_id):
    try:
        upload(order_id)
        return format('<b><font color="blue"><h2>成功</h2></font></b><br>预约号<b>{}</b>的体检报告上传成功！'.format(order_id))
    except Exception as e:
        log.error('预约号为:{}上传报告失败'.format(order_id))
        log.exception(e)
        return format(
            '<b><font color="red"><h2>失败</h2></font></b><br>预约号<b>{}</b>的体检报告上传失败!<br>{}'.format(order_id, repr(e)))
