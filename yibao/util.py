# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     redisutis
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""

from . import redis_pool
import redis
import datetime
import base64


def _get_inc():
    r = redis.Redis(connection_pool=redis_pool)
    return r.incr('yibao:msgid')


def get_msg_id(hosp_id):
    """
    获取交易id
    :param hosp_id:
    :return:
    """
    return '{}{}{}'.format(hosp_id, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), _get_inc())


def encode_base64(s):
    return str(base64.encodebytes(bytes(s, encoding='gbk')), encoding='ascii')


def decode_base64(s):
    return str(base64.decodebytes(bytes(s, encoding='ascii')), encoding='gbk')
