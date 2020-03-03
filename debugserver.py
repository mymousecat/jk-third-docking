# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     runserver
   Description :
   Author :       wdh
   date：          2019/8/28
-------------------------------------------------
   Change Activity:
                   2019/8/28:
-------------------------------------------------
"""
from app import app
from logconf import load_my_logging_cfg

load_my_logging_cfg('web_test')
if __name__ == '__main__':
    app.run(debug=True)