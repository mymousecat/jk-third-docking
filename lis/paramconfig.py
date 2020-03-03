#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/11/19 15:31

"""
  读写配置文件
"""

import json
import os
from . import appconfig


_PARAM = {
    'id':None,
    'barcodeId':None
}


_FILE = os.path.join(appconfig['CONF_PATH'],'lis_param.json')

def setValue(id,barcodeId):
    with open(_FILE,'w') as f:
        _PARAM['id'] = id
        _PARAM['barcodeId'] = barcodeId
        json.dump(_PARAM,f)

def getValue():
    if not os.path.exists(_FILE):
        return _PARAM
    else:
      with open(_FILE) as f:
            return json.load(f)
