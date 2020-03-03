# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     downloadfile
   Description :
   Author :       wdh
   date：          2019/7/31
-------------------------------------------------
   Change Activity:
                   2019/7/31:
-------------------------------------------------
"""
import re
import os
import requests
from urllib.parse import urlsplit
import filetype
import ftplib


def _getfilename(title):
    """
    去掉非法的字符
    :param filename:
    :param title:
    :return:
    """
    return re.sub(r'[\/:*?"<>|]', '-', title)  # 去掉非法字符


def _get_filepath(basedir, filenamenotext, extension):
    title = _getfilename('{}'.format(filenamenotext))
    filename = None
    if extension:
        filename = '{}.{}'.format(title, extension)
    else:
        filename = '{}'.format(title)
    return os.path.join(basedir, filename)


def _download_http_file(url, basedir, filenamenotext):
    r = requests.get(url)
    r.raise_for_status()
    # 扩展名
    ft = filetype.guess(r.content)

    path = _get_filepath(basedir, filenamenotext, ft.extension if ft else None)

    with open(path, 'wb') as f:
        for block in r.iter_content(4096):
            f.write(block)
    return path


def _download_ftp_file(url, basedir, filenamenotext, ftp_host, ftp_path, ftp_username, ftp_password, ftp_port):
    ftp = ftplib.FTP()
    ftp.connect(host=ftp_host, port=21 if ftp_port is None else ftp_port)
    if ftp_username:
        ftp.login(user=ftp_username, passwd=ftp_password)
    else:
        ftp.login()

    path = _get_filepath(basedir, filenamenotext, os.path.splitext(ftp_path)[-1].replace('.', ''))

    file_handle = open(path, 'wb').write

    # 获取文件
    ftp.retrbinary('RETR %s' % ftp_path, file_handle)

    return path


def download_file(url, basedir, filenamenotext):
    """
    下载url指定的文件
    :param url:
    :param basedir:
    :param filenamenotext:
    :return:返回文件的路径
    """
    r = urlsplit(url)
    scheme = r.scheme
    if scheme in ('http', 'https'):
        return _download_http_file(url, basedir, filenamenotext)
    elif scheme in ('ftp'):
        host = r.hostname
        path = r.path
        port = r.port
        ftp_username = r.username
        ftp_password = r.password
        return _download_ftp_file(url=url,
                                  basedir=basedir,
                                  filenamenotext=filenamenotext,
                                  ftp_host=host,
                                  ftp_path=path,
                                  ftp_username=ftp_username,
                                  ftp_password=ftp_password,
                                  ftp_port=port
                                  )
    else:
        return None
