# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     err
   Description :
   Author :       wdh
   date：          2019/8/14
-------------------------------------------------
   Change Activity:
                   2019/8/14:
-------------------------------------------------
"""

class NotFoundResultsException(Exception):
    """
    没有找到记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

class NotFoundAssemException(Exception):
    """
    没有找到记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

class NotFoundBarcodeException(Exception):
    """
    没有找到记录
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)