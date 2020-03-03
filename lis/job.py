# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     job
   Description :
   Author :       wdh
   date：          2019/8/14
-------------------------------------------------
   Change Activity:
                   2019/8/14:
-------------------------------------------------
"""

import logging
from datetime import datetime
import uuid
from . import mailtemplates, appconfig
from mail import mail

log = logging.getLogger(__name__)


def publishMail(translog):
    # 发送邮件
    if not translog.is_successfull:
        try:
            # 获取邮件模板
            s = mailtemplates.getMailTemplates(translog=translog)

            subject = "{}的项目组{}传输失败！".format(translog.username, translog.element_assem_name)

            # mail.sendMail(subject=subject, html=s, **app.config['MAIL_MSSSAGE'])

            id = 'lis_{}_{}_{}'.format(translog.barcode_id, translog.element_assem_id, str(uuid.uuid1()))

            kwargs = {
                'subject': subject,
                'html': s,
                **appconfig['MAIL_MESSAGE']
            }

            # mail.sendMail(**kwargs)
            mail.async_sendMail(**kwargs)

            # scheduler.add_job(id=id, func=mail.sendMail,
            #                   kwargs=kwargs,
            #                   trigger='date',
            #                   run_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            log.info("加入发送邮件列表成功！")

        except Exception as e:
            log.info('加入发送邮件列表失败{}'.format(repr(e)))
    else:
        log.info('条码号为:{} 项目组:{}不用发送邮件'.format(translog.barcode_id, translog.element_assem_name))
