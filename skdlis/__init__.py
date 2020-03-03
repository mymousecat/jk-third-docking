# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""

from flask import Blueprint
from .config import Config
from skdtj.skdtj import initHost

skdlis = Blueprint('skdlis', __name__, url_prefix='/skdlis')

from app import app, db, redis_pool, appconfig

app.config.from_object(Config)

initHost(appconfig['SERVER_URL'])

from . import views
