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

from jktj.downloadfile import download_file
from jktj.trans2image import trans_to_image
from jktj.uploadfile import upload_file

from . import appconfig
import logging
from urllib.parse import urljoin

log = logging.getLogger(__name__)


def upload_report(order_id, department_id, pacs_assem_id, pacs_assem_name, reporter_id, report_url, report_date):
    """
    上传体检报告图像
    :return:
    """

    if not report_url:
        log.warning('项目组id:{} 项目组名称:{}的报告url为空，无法判断上传的文件类型'.format(pacs_assem_id,pacs_assem_name))
        return

    temp_path = appconfig['TEMP_PATH']

    file_path = download_file(report_url, temp_path, '{}[{}]'.format(pacs_assem_name, order_id))

    if not file_path:
        log.warning('没有从url:{}下载到文件，可以是url无效，预约号为:{} 项目名称为:{}'.format(report_url, order_id, report_url))
        return

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
        'originalFileName': '',
        'operatorId': reporter_id
    }
    # log.warning(url)
    r = upload_file(url, images[0], params)
    log.info(r)
