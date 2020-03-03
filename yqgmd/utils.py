# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     utils
   Description :
   Author :       wdh
   date：          2019-11-01
-------------------------------------------------
   Change Activity:
                   2019-11-01:
-------------------------------------------------
"""

import datetime
import base64


def get_birthday(birthday, age):
    if birthday:
        return birthday
    else:
        return datetime.datetime.now() - datetime.timedelta(days=365 * age)


def encode_base64(bs):
    return str(base64.encodebytes(bs), encoding='gbk')


def decode_base64(s):
    return base64.decodebytes(bytes(s, encoding='ascii'))
