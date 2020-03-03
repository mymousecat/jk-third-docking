# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     downloadfile
   Description :
   Author :       wdh
   date：          2019/7/19
-------------------------------------------------
   Change Activity:
                   2019/7/19:
-------------------------------------------------
"""

from . import appconfig
import requests
import base64
from urllib.parse import urljoin
from filetype import guess

url = urljoin(appconfig['MEDIA_SERVER_URL'], 'medias_getMedia')


def download_image(media):
    params = {
        'contentType': media.content_type,
        'imageDate': media.image_date.strftime('%Y-%m-%d'),
        'departmentId': media.department_id,
        'fileExt': media.file_ext,
        'fileId': media.file_id,
        'elementAssemId': media.element_assem_id
    }

    r = requests.get(url, params)
    # 检查异常
    r.raise_for_status()

    ft = guess(r.content)
    if not ft:
        raise Exception('下载的文件类型未知')
    if ft.extension not in ['jpg', 'png', 'gif', 'tif', 'bmp', 'pdf']:
        raise Exception('下载的文件不在上传规定的范围内.[{}]'.format(ft.extension))

    # media_type = media.file_ext.replace('.', '').lower()
    return ft.extension, str(base64.encodebytes(r.content), encoding='ascii')
