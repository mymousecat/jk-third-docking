# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2020-02-07
-------------------------------------------------
   Change Activity:
                   2020-02-07:
-------------------------------------------------
"""

from flask import Blueprint
from flask_restful import Api
from .config import Config

from app import app, db, appconfig,getSession

appconfig.from_object(Config())

api = Api(app=app)

miniprog = Blueprint('miniprog', __name__, url_prefix='/api')

from . import resources, download_resources
