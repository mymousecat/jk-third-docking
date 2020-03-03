# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     config
   Description :
   Author :       wdh
   date：          2019/7/22
-------------------------------------------------
   Change Activity:
                   2019/7/22:
-------------------------------------------------
"""


class Config:
    #当前传输的项目，属于哪个科室
    DEPARTMENT = 13

    # 当前传输的项目，属于哪个项目组
    ASSEM_ID = 1006

    # 是否使用体检系统的医生,不使用的话，会新增医生，并返回ID
    PACS_USE_EXAM_DOCTOR = True
