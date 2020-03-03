#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/9/28 10:40

"""
  体检信息异常
"""

class TJException(Exception):
    """
      体检系统异常
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)



class TNetException(Exception):
    """
      网络异常或其它不能继续的异常
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return "[{0}]{1}".format(self.__class__.__name__, self.msg)
