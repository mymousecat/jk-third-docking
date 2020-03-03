# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     trans2image
   Description :
   Author :       wdh
   date：          2019/8/8
-------------------------------------------------
   Change Activity:
                   2019/8/8:
-------------------------------------------------
"""
import os
import filetype
import fitz
from PIL import Image


def _png_to_jpeg(pngfile):
    im = Image.open(pngfile)
    jpgfile = '{}.jpg'.format(pngfile)
    im.save(jpgfile)
    return jpgfile



def _pdf_to_image(filename, out_basedir):
    # pages = convert_from_path(filename,dpi=300,output_folder=out_basedir)
    # return tuple(pages)

    pages = fitz.open(filename)
    r = []
    for pg in range(0, pages.pageCount):
        page = pages[pg]
        trans = fitz.Matrix(2.78, 2.78).preRotate(0)
        pm = page.getPixmap(matrix=trans)
        path, fn = os.path.split(filename)
        fn = os.path.join(out_basedir, '{}.{}.png'.format(fn, pg + 1))
        pm.writePNG(fn)
        jpgfile = _png_to_jpeg(fn)
        r.append(jpgfile)
    return tuple(r)


def get_ext_name(bs):
    """
    获取二进制数据的文件类型
    :param bs:
    :return:
    """
    ft = filetype.guess(bs)
    if ft:
        return ft.extension
    else:
        return None


def trans_to_image(filename, out_basedir):
    """
    将不同格式的文件，转为png文件
    :param basedir:
    :param filename:
    :return:
    """
    ft = filetype.guess(filename)
    if ft:
        if ft.extension == 'pdf':
            return _pdf_to_image(filename, out_basedir)
        elif ft.extension == 'png':
            return (_png_to_jpeg(filename))
        else:
            return (filename,)

    else:
        return (filename,)
