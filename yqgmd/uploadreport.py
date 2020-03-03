# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     uploadreport
   Description :
   Author :       wdh
   date：          2019/8/22
-------------------------------------------------
   Change Activity:
                   2019/8/22:
-------------------------------------------------
"""

from jktj.trans2image import trans_to_image, get_ext_name
from jktj.uploadfile import upload_file
from .utils import decode_base64
from . import appconfig
import logging
from urllib.parse import urljoin
import os

log = logging.getLogger(__name__)


def upload_report(order_id, department_id, pacs_assem_id, pacs_assem_name, reporter_id, report_base64, report_date):
    """
    上传体检报告图像
    :return:
    """

    if not report_base64:
        log.warning('项目组id:{} 项目组名称:{}的报告Base64字符串为空，无法判断上传的文件类型'.format(pacs_assem_id, pacs_assem_name))
        return

    temp_path = appconfig['TEMP_PATH']

    report_bytes = decode_base64(report_base64)
    file_ext = get_ext_name(report_bytes)
    file_path = os.path.join(temp_path, '{}[{}]'.format(pacs_assem_name, order_id))

    if file_ext:
        file_path = '{}.{}'.format(file_path, file_ext)

    with open(file_path, 'wb') as f:
        f.write(report_bytes)


    log.info('开始转换成图像文件...')

    images = trans_to_image(file_path, temp_path)

    log.info('获取到转换后的图像列表:{}'.format(images))

    log.info('开始上传图像')

    url = urljoin(appconfig['MEDIA_SERVER_URL'], 'medias_saveMediaAndInfo')

    params = {
        'orderId': order_id,
        'imageDate': report_date.strftime('%Y-%m-%d'),
        'isUpdateExamInfo': '是',
        'departmentId': department_id,
        'elementAssemId': pacs_assem_id,
        'isPrintInReport': '是',
        'isReportPart': '否',
        'isSingle': '是',
        'originalFileName': '{}报告.jpg'.format(pacs_assem_name),
        'operatorId': reporter_id
    }

    log.info('上传图像的参数:{}'.format(params))

    # log.warning(url)
    r = upload_file(url, images[0], params)
    log.info(r)
