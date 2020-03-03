# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     err
   Description :
   Author :       wdh
   date：          2019/7/30
-------------------------------------------------
   Change Activity:
                   2019/7/30:
-------------------------------------------------
"""


class NotFoundException(Exception):
    """
    没有找到记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class InvalidMultiException(Exception):
    """
    找到多个记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class InvalidDialogException(Exception):
    """
    无效的结论
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

class InvalidOpTypeException(Exception):
    """
    无效的操作类型
    """
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

