# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :   悦绮骨密度web服务
   Author :       wdh
   date：          2019-11-01
-------------------------------------------------
   Change Activity:
                   2019-11-01:
-------------------------------------------------
"""

from flask import Blueprint
from .config import Config


yq_gmd = Blueprint('yqgmd', __name__, url_prefix='/yqgmd')

from app import app, db, redis_pool, appconfig,getSession

app.config.from_object(Config)

from . import views

