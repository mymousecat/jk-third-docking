# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     views
   Description :
   Author :       wdh
   date：          2019/8/13
-------------------------------------------------
   Change Activity:
                   2019/8/13:
-------------------------------------------------
"""

from . import lis
import logging
import re
from .translisbybarcodeid import transLisByBarcodeId
from .db_op import getBarcodeByOrderId
from .err import NotFoundBarcodeException

log = logging.getLogger(__name__)


def _build_htmls(htmls, msgs, e, order_id):
    if msgs:
        for msg in msgs:  # 格式化成html
            if msg['is_successful']:
                htmls.append("""    
                   <b>
                        <font color="blue">
                           <h2>上传成功</h2>
                        </font>
                      </b><br>
                      预约号:<b>{}</b><br>
                      姓名:<b>{}</b><br>
                      条码号:<b>{}</b><br>
                      项目组名:<b>{}</b><br>
                      <hr>                                 
                   """.format(
                    msg['examAssem'].ORDER_ID,
                    msg['examAssem'].USERNAME,
                    msg['examAssem'].BARCODE_ID,
                    msg['examAssem'].ELEMENT_NAME
                ))
            else:
                htmls.append("""
                      <b>
                        <font color="red">
                           <h2>失败</h2>
                        </font>
                      </b><br>
                      预约号:<b>{}</b><br>
                      姓名:<b>{}</b><br>
                      条码号:<b>{}</b><br>
                      项目组名:<b>{}</b><br>
                      消息:<b>{}</b><br>
                      <hr>                                 
                   """.format(
                    msg['examAssem'].ORDER_ID,
                    msg['examAssem'].USERNAME,
                    msg['examAssem'].BARCODE_ID,
                    msg['examAssem'].ELEMENT_NAME,
                    msg['msg']
                )
                )
    elif e:
        if order_id:
            htmls.append("""
              <b><font color="red"><h2>失败</h2></font></b><br>
              预约号:{}<br>
              LIS结果上传失败!<br>{}<br><hr>               
           """.format(order_id, repr(e)))
        else:
            htmls.append('<b><font color="red"><h2>失败</h2></font></b><br>LIS结果上传失败!<br>{}<hr>'.format(repr(e)))


@lis.route('/oids/<order_ids>')
def trans_lis_by_order_ids(order_ids):
    """
    多个预约号分割，使用逗号分割
    :param order_ids:
    :return:
    """
    order_id_list = re.split(r',|，|\^|\|', order_ids)
    log.info('获取到多个预约号:{}'.format(order_id_list))

    htmls = []
    msgs = []

    for order_id in order_id_list:
        try:
            barcodes = getBarcodeByOrderId(order_id)
            if len(barcodes) == 0:
                raise NotFoundBarcodeException('预约号为:{}在体检系统中不存在条码号'.format(order_id))

            for barcode in barcodes:
                try:
                    l = transLisByBarcodeId(barcode, None)
                    msgs.extend(l)
                except Exception as e:
                    _build_htmls(htmls, None, e, order_id)
        except Exception as e:
            _build_htmls(htmls, None, e, order_id)

    _build_htmls(htmls, msgs, None, None)

    return '\n'.join(htmls)


@lis.route('/<barcodes>')
def trans_lis_by_barcodes(barcodes):
    """
    多个条码分割,使用逗号分隔
    :param barcodes:
    :return:
    """
    barcode_list = re.split(r',|，|\^|\|', barcodes)
    log.info('获取到多个条码:{}'.format(barcode_list))

    htmls = []
    msgs = []

    for barcode in barcode_list:
        try:
            l = transLisByBarcodeId(barcode.strip(), None)
            msgs.extend(l)
        except Exception as e:
            _build_htmls(htmls, None, e, None)

    _build_htmls(htmls, msgs, None, None)

    return '\n'.join(htmls)
