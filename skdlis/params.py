# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     params
   Description :
   Author :       wdh
   date：          2019/3/15
-------------------------------------------------
   Change Activity:
                   2019/3/15:
-------------------------------------------------
"""
from . import appconfig
import os
import json


class CurPosParams:
    """
      记录和读取当前位置信息
    """

    def __init__(self):
        self._filename = os.path.join(appconfig['CONF_PATH'], 'skdlis_pos_param.json')
        self._r = {'curPos': None}

    def save(self, pos):
        self._r['curPos'] = pos
        with open(self._filename, 'w') as f:
            json.dump(self._r, f)

    def get(self):
        if not os.path.exists(self._filename):
            return None
        with open(self._filename, 'r') as f:
            try:
                r = json.load(f)
                return r['curPos']
            except:
                return None
