# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2019/8/13
-------------------------------------------------
   Change Activity:
                   2019/8/13:
-------------------------------------------------
"""

from flask import Blueprint
from .config import Config


lis = Blueprint('lis', __name__, url_prefix='/lis')

from app import app, db, redis_pool, appconfig,getSession

app.config.from_object(Config)

from . import views

