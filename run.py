# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     run
   Description :
   Author :       wdh
   date：          2019/8/28
-------------------------------------------------
   Change Activity:
                   2019/8/28:
-------------------------------------------------
"""

from app import app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from logconf import load_my_logging_cfg

load_my_logging_cfg('web')
if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000, '0.0.0.0')
    IOLoop.instance().start()
