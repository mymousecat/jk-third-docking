# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019-11-01
-------------------------------------------------
   Change Activity:
                   2019-11-01:
-------------------------------------------------
"""

from .models import YQGmdView
from . import db


def get_gmd_by_patient(patient_id):
    try:
        return db.session.query(YQGmdView).filter(YQGmdView.PatientID == patient_id).all()
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        db.session.close()
