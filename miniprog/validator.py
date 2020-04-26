# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     validator
   Description :
   Author :       wdh
   date：          2019/2/13
-------------------------------------------------
   Change Activity:
                   2019/2/13:
-------------------------------------------------
"""

import datetime


def date(strDate):
    try:
        datetime.datetime.strptime(strDate, '%Y-%m-%d')
        return strDate
    except:
        raise Exception("{} is not a valid Date".format(strDate))


def validCert(certId):
    if len(certId) != 18:
        raise Exception("无效的身份证号")
    cert = certId.upper().strip()
    ID_check = cert[17]
    W = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # ID_num = [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    ID_CHECK = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    ID_aXw = 0
    for i in range(len(W)):
        ID_aXw = ID_aXw + int(cert[i]) * W[i]
    ID_Check = ID_aXw % 11
    if ID_check != ID_CHECK[ID_Check]:
        raise Exception("无效的身份证号")
    return cert

def getInfo(certId):
    # 130406197411063315
    strBirth = certId[6:14]
    strSex = certId[14:17]
    birth = '{}-{}-{}'.format(strBirth[0:4], strBirth[4:6], strBirth[6:])
    sex = None
    if int(strSex) % 2 == 0:
        sex = '2'
    else:
        sex = '1'
    return {'birth': birth, 'sex': sex}

