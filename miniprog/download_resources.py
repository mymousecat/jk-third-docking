# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     download_resources
   Description :
   Author :       wdh
   date：          2019/9/8
-------------------------------------------------
   Change Activity:
                   2019/9/8:
-------------------------------------------------
"""

from flask_restful import Resource
from flask import Response
from jktj.jktj import download_pdf
from .resources import _loginTj, dealException
from . import api
import logging
import base64

log = logging.getLogger(__name__)


class PDFApi(Resource):
    def get(self, orderId):
        """
        开始下载pdf报告
        :param order_id:
        :return:
        """
        try:
            _loginTj()
            r = download_pdf(orderId)
            log.info('下载预约号为:{}的pdf报告成功！'.format(orderId))
            # response = Response(r.content,content_type=r.headers['Content-Type'])
            # response.headers['Content-disposition'] = 'attachment; filename=长海体检中心-体检报告【{}】.pdf'.format(orderId).encode('utf8')
            # return response
            # 编码为base64
            # return str(base64.b64encode(r.content),encoding='utf-8')
            response = Response(str(base64.b64encode(r.content),encoding='utf-8'),content_type='text/plain')
            return response


        except Exception as e:
            dealException(e)


api.add_resource(PDFApi,
                 '/api/v1.0/pdfReport/<int:orderId>',
                 endpoint='pdfreport'
                 )
