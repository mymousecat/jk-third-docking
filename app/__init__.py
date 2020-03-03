# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2019/7/20
-------------------------------------------------
   Change Activity:
                   2019/7/20:
-------------------------------------------------
"""

# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""

# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     __init__.py
   Description :   青岛城投体检中心、委计卫公务员数据对接
   Author :       wdh
   date：          2019/4/12
-------------------------------------------------
   Change Activity:
                   2019/4/12:
-------------------------------------------------
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import redis
from jktj.jktj import initHost

app = Flask(__name__)
app.config.from_object(Config())


# 跨域支持
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)
db = SQLAlchemy(app=app)

redis_pool = redis.ConnectionPool(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)

appconfig = app.config

initHost(appconfig['SERVER_URL'])

# 注册蓝图

# # 医保
# from yibao import yibao
#
# app.register_blueprint(yibao)
#
# # pacs
# from pacs import pacs
#
# app.register_blueprint(pacs)

# lis
# from lis import lis
#
# app.register_blueprint(lis)

# 悦绮骨密度
# from yqgmd import yq_gmd
#
# app.register_blueprint(yq_gmd)

# skdlis
# from skdlis import skdlis

# app.register_blueprint(skdlis)

# miniprog
from miniprog import miniprog

app.register_blueprint(miniprog)


from . import views
