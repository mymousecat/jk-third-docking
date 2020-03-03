# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     xml_util
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""
from .err import XMLException

import lxml.html

etree = lxml.html.etree


def _getElement(tree, path):
    if tree is not None:
        nodes = tree.xpath(path)
        if len(nodes) > 0:
            return nodes[0]


def getElement(tree, path):
    e = _getElement(tree, path)
    if e is None:
        raise XMLException('路径{0}不存在，无效的输入XML'.format(path))
    else:
        return e


def addElement(tree, path, newNodeName, text=None, notnull=True):
    e = getElement(tree, path)
    child = etree.SubElement(e, newNodeName)
    if text is not None:
        child.text = str(text)
    elif notnull:
        raise XMLException('节点[{}]的值不能为空'.format(newNodeName))
    return child


def addElementByNode(node, newNodeName, text=None, notnull=True):
    if node is not None:
        child = etree.SubElement(node, newNodeName)
        if text is not None:
            child.text = str(text)
        elif notnull:
            raise XMLException('节点[{}]的值不能为空'.format(newNodeName))
        return child

