# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     err
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""


class NotFoundLisResultException(Exception):
    """
    没有找到记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class TjAssemResultsException(Exception):
    """
    上传项目组结果导常
    """

    def __init__(self, order_id, username, sex_name, age, assem_id, assem_name, msg):
        self.order_id = order_id
        self.username = username
        self.sex_name = sex_name
        self.age = age
        self.assem_id = assem_id
        self.assem_name = assem_name
        self.msg = msg

    def __repr__(self):
        return "[{}]  \n {}".format(self.__class__.__name__, self.msg)


class Success:
    """
    上传项目组成功
    """

    def __init__(self, order_id, username, sex_name, age, assem_id, assem_name):
        self.order_id = order_id
        self.username = username
        self.sex_name = sex_name
        self.age = age
        self.assem_id = assem_id
        self.assem_name = assem_name
        self.msg = '传输成功'
