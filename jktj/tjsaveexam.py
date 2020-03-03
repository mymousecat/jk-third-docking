#!/usr/bin/env python
# encoding: utf-8
# author: Think
# created: 2018/10/5 10:16

"""
  保存体检结果数据
"""

import time


def _getElementAssemByCode(exam, elementAssemId=None):
    if not elementAssemId:
        return exam['assems'][0]
    else:
        for assem in exam['assems']:
            if str(assem['assemId']) == elementAssemId:
                return assem


def getElementAssemByCode(exam, elementAssemId=None):
    return _getElementAssemByCode(exam, elementAssemId)


def initSaveExam(exam, deprtId, opId, addOpId, saveSymbol="提交"):
    """
    初始化保存数据
    :param exam:
    :param saveSymbol:
    :return:
    """
    saveExam = {}
    if exam:
        saveExam['saveSymbol'] = saveSymbol
        saveExam['orderId'] = exam['orderId']
        saveExam['deptId'] = deprtId
        saveExam['opId'] = opId
        saveExam['addOpId'] = addOpId
        saveExam['posReport'] = {'content': '',
                                 'advice': None,
                                 'opId': None,
                                 'opTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                                 }
        saveExam['elements'] = []
        saveExam['assems'] = []
    return saveExam


def addPosReport(saveExam, content, advice=None, optime=None, opId=None):
    saveExam['posReport']['content'] = content
    saveExam['posReport']['advice'] = advice
    if optime:
        saveExam['posReport']['optime'] = optime
    else:
        saveExam['posReport']['optime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    saveExam['posReport']['opId'] = opId

    # posReport = {}
    #
    #
    #
    # posReport['content'] = content
    # posReport['advice'] = advice
    # posReport['opId'] = opId
    # if optime:
    #     posReport['opTime'] = optime
    # else:
    #     posReport['opTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # saveExam['posReport']=[]
    # saveExam['posReport'].append(posReport)


def _getSaveAssem(saveExam, exam, deptId, opId, examAssem):
    assem = None

    for e in saveExam['assems']:
        if e['assemId'] == examAssem['assemId']:
            assem = e
            break

    if assem is None:
        assem = {}
        assem['loginTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        assem['orderId'] = exam['orderId']
        assem['assemId'] = examAssem['assemId']
        assem['deptId'] = deptId
        assem['opId'] = opId
        assem['completeTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        assem['summaryDetas'] = []
        saveExam['assems'].append(assem)
    return assem


def addElementResult(saveExam, exam, opId, elementAssemId=None, **kwargs):
    examAssem = _getElementAssemByCode(exam, elementAssemId)
    # 修改小项的默认值或值
    for examElement in examAssem['elements']:
        element = {}
        element['opId'] = opId
        element['assemId'] = examAssem['assemId']
        element['elementId'] = examElement['elementId']
        element['resultType'] = examElement['resultType']
        element['unit'] = examElement['unit']
        element['refLower'] = examElement['refLower']
        element['refUpper'] = examElement['refUpper']
        element['positiveSymbol'] = examElement['positiveSymbol']
        element['refType'] = examElement['refType']
        element['giveUp'] = False
        element['resultId'] = None
        element['result'] = examElement['defVal']
        if kwargs:
            key = str(element['elementId'])
            if key in kwargs.keys():
                element['result'] = kwargs[key]
            elif 'others' in kwargs.keys():
                element['result'] = kwargs['others']


        saveExam['elements'].append(element)


def addDefaut(saveExam, exam, deptId, opId, elementAssemId=None, result=None):
    examAssem = _getElementAssemByCode(exam, elementAssemId)
    assem = _getSaveAssem(saveExam, exam=exam, deptId=deptId, opId=opId, examAssem=examAssem)
    # 加入默认小节
    summaryDeta = {}
    summaryDeta['content'] = examAssem['defSummary']
    summaryDeta['result'] = result
    summaryDeta['proposal'] = None
    summaryDeta['writeSymbol'] = '03'
    summaryDeta['doubtSymbol'] = False
    summaryDeta['positions'] = None
    summaryDeta['mergeWord'] = examAssem['defSummary']
    assem['summaryDetas'].append(summaryDeta)


def addDisease(saveExam, exam, deptId, opId, writeSymbol, diseaseName, diseaseCode, elementAssemId=None, result=None):
    examAssem = _getElementAssemByCode(exam, elementAssemId)
    assem = _getSaveAssem(saveExam, exam=exam, deptId=deptId, opId=opId, examAssem=examAssem)
    # 加入疾病
    summaryDeta = {}
    summaryDeta['content'] = diseaseCode
    summaryDeta['result'] = result
    summaryDeta['proposal'] = None
    summaryDeta['writeSymbol'] = writeSymbol
    summaryDeta['doubtSymbol'] = False
    summaryDeta['positions'] = None
    summaryDeta['mergeWord'] = diseaseName
    assem['summaryDetas'].append(summaryDeta)
