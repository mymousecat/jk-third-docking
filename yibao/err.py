# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     err
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""


class XMLException(Exception):
    """
      XML输入异常
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class NotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)


class InValidException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

class InvokeException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)

class NotFoundNewTransLogException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)