# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     test2
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""

from skdlis.transbyorderid import trans_skdlis_by_order_id
from logconf import load_my_logging_cfg

load_my_logging_cfg('test2')
if __name__ == '__main__':
    trans_skdlis_by_order_id(1003402)