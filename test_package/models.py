# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2020-11-11
-------------------------------------------------
   Change Activity:
                   2020-11-11:
-------------------------------------------------
"""
from app import db

class TestModel(db.Model):
    __tablename__ = 't_test'
    id = db.Column(db.Integer,primary_key=True)
    test = db.Column(db.String)


