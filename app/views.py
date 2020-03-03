# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019/7/20
-------------------------------------------------
   Change Activity:
                   2019/7/20:
-------------------------------------------------
"""

import os
from flask import send_from_directory
from . import app


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
