
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :   廊坊医保数据对接
   Author :       wdh
   date：          2019/4/12
-------------------------------------------------
   Change Activity:
                   2019/4/12:
-------------------------------------------------
"""

from flask import Blueprint
from .config import Config

yibao = Blueprint('yibao', __name__, url_prefix='/yibao')

from app import app ,db, redis_pool, appconfig

app.config.from_object(Config)


from . import views
