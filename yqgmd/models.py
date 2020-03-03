# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       wdh
   date：          2019-11-01
-------------------------------------------------
   Change Activity:
                   2019-11-01:
-------------------------------------------------
"""

from . import db


class YQGmdView(db.Model):
    """
      PACS结果表
    """
    __tablename__ = 'v_gmd'
    PatientID = db.Column(db.String, primary_key=True)
    NAME = db.Column(db.String)
    Gender = db.Column(db.String)
    Birthday = db.Column(db.Date)
    Age = db.Column(db.Integer)
    RequstDate = db.Column(db.Date)
    RequstDepartment = db.Column(db.String)
    RequestDoctor = db.Column(db.String)
    Weight = db.Column(db.String)
    Height = db.Column(db.String)
