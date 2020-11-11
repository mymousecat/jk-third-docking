# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     trans_lis
   Description :
   Author :       wdh
   date：          2019/7/20
-------------------------------------------------
   Change Activity:
                   2019/7/20:
-------------------------------------------------
"""

import logging
from logconf import load_my_logging_cfg
from apscheduler.schedulers.blocking import BlockingScheduler

# from lis.task import autoTransLis
# from yibao.task import yibaoTrans
# from pacs.task import autoTransPacsReg, autoTransPacsResult
# from skdlis.task import autoTransSkdLis


from test_package.db_op import add
from app import app
from flask_script import Manager, Command

log = logging.getLogger(__name__)

manager = Manager(app)


def _get_scheduler():
    return BlockingScheduler(
        executors=app.config['SCHEDULER_EXECUTORS'],
        job_defaults=app.config['SCHEDULER_JOB_DEFAULTS'])


def _begin_scheduler(scheduler):
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info('任务结束.')
        scheduler.shutdown()


class Test(Command):
    """
    测试作务
    """
    def run(self):
        load_my_logging_cfg('test_package_trans')
        ## 每1秒一次
        scheduler = _get_scheduler()
        scheduler.add_job(add, id='trans_test_package', trigger='cron', second='*/1', replace_existing=True)
        _begin_scheduler(scheduler)



# class Lis(Command):
#     """
#     LIS传输
#     """
#     def run(self):
#         load_my_logging_cfg('lis_trans')
#         # # 第10秒一次
#         scheduler = _get_scheduler()
#         scheduler.add_job(autoTransLis, id='trans_to_lis_ex', trigger='cron', second='*/10', replace_existing=True)
#         _begin_scheduler(scheduler)


# class Pacs(Command):
#     """
#     PACS结果传输
#     """
#
#     def run(self):
#         load_my_logging_cfg('pacs_result_trans')
#         scheduler = _get_scheduler()
#         scheduler.add_job(autoTransPacsResult, id='trans_pacs_result', trigger='cron', day='*', second='*/10',
#                           replace_existing=True)
#         _begin_scheduler(scheduler)
#
#
# class PacsReg(Command):
#     """
#     PACS登记
#     """
#
#     def run(self):
#         load_my_logging_cfg('pacs_reg_trans')
#         scheduler = _get_scheduler()
#         scheduler.add_job(autoTransPacsReg, id='trans_pacs_reg', trigger='cron', day='*', second='*/10',
#                           replace_existing=True)
#         _begin_scheduler(scheduler)
#
#
# class Yiabo(Command):
#     """
#     医保数据传输
#     """
#
#     def run(self):
#         load_my_logging_cfg('yibao_trans')
#         scheduler = _get_scheduler()
#         # hour = '19-23,0-6'
#         scheduler.add_job(yibaoTrans, id='trans_exam_yibao', trigger='cron', day='*', hour='19-23,0-6', minute='*/1',
#                           replace_existing=True)
#         _begin_scheduler(scheduler)
#

# class SkdLis(Command):
#     """
#     原圣康达lis传输 二炮体检中心 从检验科
#     """
#
#     def run(self):
#         load_my_logging_cfg('skdlis_trans')
#         scheduler = _get_scheduler()
#         # hour = '19-23,0-6'
#         scheduler.add_job(autoTransSkdLis, id='trans_skdlis', trigger='cron', day='*', second='*/10',
#                           replace_existing=True)
#         _begin_scheduler(scheduler)


# manager.add_command('lis', Lis())
#manager.add_command('pacs', Pacs())
#manager.add_command('pacsreg', PacsReg())
#manager.add_command('yibao', Yiabo())
# manager.add_command('skdlis', SkdLis())

manager.add_command('test',Test())

if __name__ == '__main__':
    manager.run()
