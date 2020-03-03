# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     jsonencoder
   Description :
   Author :       wdh
   date：          2020-02-12
-------------------------------------------------
   Change Activity:
                   2020-02-12:
-------------------------------------------------
"""
import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


def _convertObj(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    else:
        return obj


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):

        # elif isinstance(obj, InstanceState):
        #     return None
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if
                          not x.startswith('_') and x != 'metadata' and x not in ('query', 'query_class')]:
                data = obj.__getattribute__(field)
                try:
                    # d = json.dumps(data,
                    #                cls=DatetimeEncoder)  # this will fail on non-encodable values, like other
                    o = _convertObj(data)
                    fields[field] = o
                except TypeError:
                    fields[field] = None

            # a json-encodable dict
            return fields
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return obj

        return json.JSONEncoder.default(self, obj)
