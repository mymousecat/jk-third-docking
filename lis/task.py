# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     task
   Description :
   Author :       wdh
   date：          2019/8/14
-------------------------------------------------
   Change Activity:
                   2019/8/14:
-------------------------------------------------
"""

from .paramconfig import getValue
import logging
from datetime import datetime
from .db_op import getNextBarcode, need_push_mail, saveLisTransLog
from .models import LisTransLog
from . import appconfig
from .translisbybarcodeid import transLisByBarcodeId
from .job import publishMail
from .err import NotFoundResultsException, NotFoundAssemException

log = logging.getLogger(__name__)


def _saveTransLog(examAssem, sample_date, operator_id, operator_name, is_successful, msg):
    translog = LisTransLog()
    translog.order_id = examAssem.ORDER_ID
    translog.barcode_id = examAssem.BARCODE_ID

    translog.element_assem_id = examAssem.ELEMENT_ID
    translog.element_assem_name = examAssem.ELEMENT_NAME

    translog.username = examAssem.USERNAME
    translog.sex_name = examAssem.SEX_NAME
    translog.age = examAssem.AGE

    translog.operator_id = operator_id if operator_id is not None else 0

    translog.operator_name = operator_name if operator_name is not None else '系统自动'

    translog.sample_date = sample_date if sample_date is not None else datetime.now()
    translog.is_successfull = is_successful
    translog.trans_msg = msg

    translog.trans_time = datetime.now()
    translog.trans_date = datetime.now()

    # if not translog.is_successfull:

    saveLisTransLog(translog)

    # 是否发送发送邮件
    if appconfig['IS_SEND_MAIL'] and need_push_mail(translog.barcode_id, translog.element_assem_id):
        publishMail(translog)


def autoTransLis():
    """
    自动传输LIS数据到体检系统中
    :return:
    """
    try:
        log.info('开始从配置文件获取ID和条码号...')
        config = getValue()
        log.info('从配置文件获取到ID:{} 条码号为:{}'.format(config['id'], config['barcodeId']))
        cur_id = 0 if config['id'] is None else config['id']
        log.info('开始从HIS系统中获取LIS结果数据...')
        barcodeId = getNextBarcode(config['id'], config['barcodeId'])
        log.info('获取到的barcode值为:{}'.format(barcodeId))
        if barcodeId is None:
            log.info('没有获取到最新的barcode值，程序将返回...')
            return

        msgs = transLisByBarcodeId(barcodeId=barcodeId, cur_id=cur_id)

        for msg in msgs:
            _saveTransLog(
                examAssem=msg['examAssem'],
                sample_date=msg['sample_date'],
                operator_id=msg['operator_id'],
                operator_name=msg['operator_name'],
                is_successful=msg['is_successful'],
                msg=msg['msg'] if msg['str_item_results'] is None else msg['msg'] + '\n' + msg['str_item_results']
            )

    except (NotFoundResultsException, NotFoundResultsException) as e:
        log.log(repr(e))

    except Exception as e:
        log.exception(e)
