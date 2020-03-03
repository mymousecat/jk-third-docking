# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       wdh
   date：          2019/8/13
-------------------------------------------------
   Change Activity:
                   2019/8/13:
-------------------------------------------------
"""

class Config:
    #第三方数据库(his)
    LIS_USERNAME_CONST = "tjuser"
    LIS_PASSWORD_CONST = "1234"
    LIS_HOST_CONST = "172.20.111.240"
    LIS_DATABASE_CONST = "his_fee"

    SQLALCHEMY_BINDS = {
        # 'jk': 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
        #     JK_USERNAME_CONST, JK_PASSWORD_CONST, JK_HOST_CONST, JK_DATABASE_CONST),
        # 'his': 'oracle://%s:%s@%s/%s?charset=gbk' % (
        #     HIS_USERNAME_CONST, HIS_PASSWORD_CONST, HIS_HOST_CONST, HIS_DATABASE_CONST)
        'lis': 'mssql+pymssql://%s:%s@%s/%s' % (
            LIS_USERNAME_CONST, LIS_PASSWORD_CONST, LIS_HOST_CONST, LIS_DATABASE_CONST)
    }


