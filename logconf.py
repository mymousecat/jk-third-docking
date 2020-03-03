#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/9/21 11:31

"""
logging日志配置
"""

import os
import logging.config

# 定义三种日志输出格式 开始
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'


# 定义日志输出格式 结束

def _getLogName(logname):
    logfile_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'log'))  # log文件的目录

    logfile_name = None
    if logname:
        logfile_name = '{}.log'.format(logname)
    else:
        logfile_name = 'all.log'  # log文件名

    # 如果不存在定义的日志目录就创建一个
    if not os.path.isdir(logfile_dir):
        os.mkdir(logfile_dir)

    # log文件的全路径
    return os.path.join(logfile_dir, logfile_name)


def _getLogDic(logname):
    # log配置字典
    LOGGING_DIC = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': standard_format
            },
            'simple': {
                'format': simple_format
            },
        },
        'filters': {},
        'handlers': {
            # 打印到终端的日志
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',  # 打印到屏幕
                'formatter': 'simple'
            },
            # 打印到文件的日志,收集info及以上的日志
            'default': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'formatter': 'standard',
                'filename': logname,  # 日志文件
                'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                'backupCount': 5,
                'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
            },

            # 记录错误的日志
            'err': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                'formatter': 'standard',
                'filename': '{}_err{}'.format(os.path.splitext(logname)[0], os.path.splitext(logname)[-1]),  # 日志文件
                'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                'backupCount': 5,
                'encoding': 'utf-8',
            },

        },
        'loggers': {
            # logging.getLogger(__name__)拿到的logger配置
            '': {
                'handlers': ['default', 'console', 'err'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                'level': 'DEBUG',
                'propagate': True,  # 向上（更高level的logger）传递
            },
        },
    }

    return LOGGING_DIC


def load_my_logging_cfg(logname=None):
    log_name = _getLogName(logname)
    logging.config.dictConfig(_getLogDic(log_name))  # 导入上面定义的logging配置
