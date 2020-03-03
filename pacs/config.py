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
    # PACS传输的科室范围,6-DR,20-CT,21-MR,33-PET
    DEPARTMENTS_RANGE = (6, 20, 21)

    #项目组对照码，就是项目组ID
    MAP_CODE_IS_ASSEM_ID = True

    # 是否使用体检系统的医生,不使用的话，会新增医生，并返回ID
    PACS_USE_EXAM_DOCTOR = False


