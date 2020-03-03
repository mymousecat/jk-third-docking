# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     translisbybarcodeid
   Description :
   Author :       wdh
   date：          2019/8/14
-------------------------------------------------
   Change Activity:
                   2019/8/14:
-------------------------------------------------
"""

from .err import NotFoundResultsException, NotFoundAssemException
from .db_op import getItems, getAssems
import logging
from .paramconfig import setValue
from .translisbyassem import transLisByAssem
from jktj.tjexception import TJException

log = logging.getLogger(__name__)


def _get_next_id(cur_id, lis_result_ids):
    if cur_id is not None:
        ids = [x for x in lis_result_ids if x > cur_id]
        ids.sort()
        l0 = len(ids) - 1
        if l0 == 0:
            return ids[0]
        while l0 > 0:
            if ids[l0] - ids[0] == l0:
                return ids[l0]
            l0 = l0 - 1
        return ids[0]
    else:
        return None


def _buildReturn(examAssem, sample_date, operator_id, operator_name, is_successful, msg, str_item_results):
    _r = {
        'examAssem': examAssem,
        'sample_date': sample_date,
        'operator_id': operator_id,
        'operator_name': operator_name,
        'is_successful': is_successful,
        'msg': msg,
        'str_item_results': str_item_results
    }
    return _r


def transLisByBarcodeId(barcodeId, cur_id):
    log.info('开始从体检系统中获取项目组信息，条码号为:{}'.format(barcodeId))
    assems = getAssems(barcodeId)

    assem_names = ','.join([assem.ELEMENT_NAME for assem in assems])

    log.info('从LIS系统中获取项目结果,条码号为{}'.format(barcodeId))
    lisResultItems = getItems(barcodeId)
    log.info('从HIS获取了{}条项目结果'.format(len(lisResultItems)))
    if len(lisResultItems) == 0:
        raise NotFoundResultsException('没有从LIS系统中获取到项目结果,条码号为{},对应的项目组:{}'.format(barcodeId, assem_names))

    lis_result_ids = []
    lis_result_dict = {}

    for lisResult in lisResultItems:
        lis_result_ids.append(lisResult.ID)
        if lisResult.LIS_ELEMENT_ID is not None:
            key = str(lisResult.LIS_ELEMENT_ID)
            lis_result_dict[key] = lisResult

    nextId = _get_next_id(cur_id, lis_result_ids)

    sample_date = lisResultItems[0].SAMPLE_DATE

    if len(assems) == 0:
        if nextId is not None:
            setValue(nextId, barcodeId)
        log.error('没有从体检系统中获取条码号为{}的项目组信息，下一个ID为{}，程序将退出...'.format(barcodeId, nextId))
        raise NotFoundAssemException('没有从体检系统中获取条码号为{}的项目组信息'.format(barcodeId))

    log.info('开始分析体检项目数据...')

    returnMsg = []

    for assem in assems:
        try:
            str_item_results = transLisByAssem(assem.DEPARTMENT_ID, assem.ORDER_ID, assem.ELEMENT_ID, lis_result_dict)
            # 如果保存成功
            msg = '条码号:{} 预约号:{} 项目组ID:{} 项目组名:{}保存LIS数据成功'.format(assem.BARCODE_ID,
                                                                   assem.ORDER_ID,
                                                                   assem.ELEMENT_ID,
                                                                   assem.ELEMENT_NAME)
            log.info(msg)
            returnMsg.append(_buildReturn(assem, sample_date, None, None, True,
                                          '保存LIS数据成功!', str_item_results))
        except TJException as e:
            msg = '条码号:{} 预约号:{} 项目组ID:{} 项目组名:{}保存LIS数据失败!【{}】'.format(assem.BARCODE_ID,
                                                                        assem.ORDER_ID,
                                                                        assem.ELEMENT_ID,
                                                                        assem.ELEMENT_NAME, repr(e))
            log.error(msg)
            returnMsg.append(_buildReturn(assem, sample_date, None, None, False,
                                          repr(e), None))

    if nextId is not None:
        setValue(nextId, barcodeId)

    return returnMsg
