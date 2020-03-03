#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/12/7 10:49


"""
  生成邮件模板
"""

from jinja2 import PackageLoader,Environment


def getMailTemplates(**kwargs):
    env = Environment(loader=PackageLoader('lis','templates'))
    template = env.get_template('mail.html')
    return template.render(**kwargs)
