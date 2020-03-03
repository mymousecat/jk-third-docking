# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       wdh
   date：          2020-02-12
-------------------------------------------------
   Change Activity:
                   2020-02-12:
-------------------------------------------------
"""

from .jsonencoder import CJsonEncoder

class Config:
    # 体检系统客户来源
    TJ_CUSTOMER_SOURCE = '07'

    RESTFUL_JSON = {
        'ensure_ascii': False,
        'cls': CJsonEncoder
    }