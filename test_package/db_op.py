# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2020-11-11
-------------------------------------------------
   Change Activity:
                   2020-11-11:
-------------------------------------------------
"""
from app import db
from .models import TestModel
import uuid
import logging

log = logging.getLogger(__name__)

def _getSession():
    return db.create_scoped_session()

import string
import random

def _getrandom():
    TEXT = string.punctuation + string.ascii_letters + string.digits

    s = ''
    for i in range(random.randint(1,10)):
        s = s + ''.join(random.sample(TEXT,k=32))

    return s



def add():
    session = _getSession()
    try:
        m = TestModel()
        test = _getrandom()
        m.test = test
        log.info('获取新的test:{}'.format(test))
        session.add(m)
        session.commit()
        log.info('')
    finally:
        session.close()
