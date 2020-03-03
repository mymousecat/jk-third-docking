# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     uploadfile
   Description :
   Author :       wdh
   date：          2019/7/31
-------------------------------------------------
   Change Activity:
                   2019/7/31:
-------------------------------------------------
"""

import requests
from .jktj import tjAssert
import logging

log = logging.getLogger(__name__)


def upload_file(url, filename, params):
    f = open(filename, 'rb')
    try:
        files = {
            'file': (filename, f, 'application/octet-stream')
        }
        r = requests.post(url=url, data=params, files=files)
        data = r.json()
        return tjAssert(data)
    finally:
        if f:
            f.close()
