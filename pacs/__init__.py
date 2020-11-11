# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :  第三方PACS与体检系统对接
   Author :       wdh
   date：          2019/7/22
-------------------------------------------------
   Change Activity:
                   2019/7/22:
-------------------------------------------------
"""

from flask import Blueprint
from .config import Config


pacs = Blueprint('pacs', __name__, url_prefix='/pacs')

from app import app, db, redis_pool, appconfig,getSession

app.config.from_object(Config())

from . import views
