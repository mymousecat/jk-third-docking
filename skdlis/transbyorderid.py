# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     transbyorderid
   Description :
   Author :       wdh
   date：          2019/8/27
-------------------------------------------------
   Change Activity:
                   2019/8/27:
-------------------------------------------------
"""

import logging
from skdtj.skdtj import get_person_info, tjAssert, login, get_exam_item_result, get_user_info, save_lis
from skdtj.tjexception import TJException
from .db_op import get_lis_result
from . import appconfig
from .params import CurPosParams
from .err import NotFoundLisResultException, TjAssemResultsException, Success
import re

log = logging.getLogger(__name__)

SKD_TJ_NAME = appconfig['JK_EXAM_USERNAME']
SKD_TJ_PASSWORD = appconfig['JK_EXAM_PASSWORD']
LIS_DEPARTMENTS = appconfig['LIS_DEPARTMENTS']


def trans_skdlis_by_order_id(order_id, cur_id):
    msgs = []
    next_id = None
    try:
        log.info('开始在lis中查询预约号为：{}的结果...'.format(order_id))
        lis_results = get_lis_result(order_id)
        if not lis_results:
            raise NotFoundLisResultException('在LIS中，没有找到预约号为:{}的结果记录.'.format(order_id))

        log.info('从lis中，获取到{}条记录'.format(len(lis_results)))

        lis_result_dict = {}
        lis_result_ids = []

        for result in lis_results:
            key = str(result.LIS_ELEMENT_ID)
            lis_result_dict[key] = result
            lis_result_ids.append(result.ID)

        next_id = _get_next_id(cur_id, lis_result_ids)

        log.info('获取下一个ID为:{}'.format(next_id))

        _loginTj()
        log.info('开始获取预约号为:{}的个人信息..'.format(order_id))
        userinfo = tjAssert(get_person_info(order_id))['msg']
        username = userinfo['username']
        age = userinfo['age']
        sex_name = userinfo['sex']

        log.info('获取到个人基本信息,姓名:{} 年龄:{} 性别:{}'.format(username, age, sex_name))

        for department in LIS_DEPARTMENTS:
            try:
                log.info('开始根据科室id:{}，获取检验结果信息..'.format(department))
                assem_items_info = tjAssert(get_exam_item_result(order_id, department, None))['msg']
                log.info('获取到项目结果数据:{}'.format(assem_items_info))
                items_dict = {}
                assem_name_dict = {}
                for item in assem_items_info:
                    if item['rowType'] == 'item':
                        key = str(item['itemComId'])
                        if key not in items_dict.keys():
                            items_dict[key] = []
                        items_dict[key].append(item)
                    elif item['rowType'] == 'group':
                        key = str(item['comId'])
                        if key not in assem_name_dict.keys():
                            assem_name_dict[key] = item['name']

                for assem_id in items_dict.keys():
                    assem_name = assem_name_dict[assem_id]
                    log.info(
                        '开始上传项目组，预约号:{} 科室id:{} 项目组id:{}  项目组名称:{}'.format(order_id, department, assem_id, assem_name))
                    try:
                        trans_skdlis_by_assem(order_id, username, sex_name, age, department, assem_id, assem_name,
                                              items_dict[assem_id],
                                              lis_result_dict
                                              )

                        # 传输项目组成功
                        msgs.append(Success(order_id, username, sex_name, age, assem_id, assem_name))

                    except TjAssemResultsException as e:
                        msgs.append(e)
                        msg = '预约号：{} 科室ID:{}  项目组id:{} 项目组名称:{}  原因:{} 从体检系统获取科室项目失败'.format(order_id, department,
                                                                                              assem_id,
                                                                                              assem_name,
                                                                                              repr(e))
                        log.error(msg)
                        log.exception(e)


            except TJException as e:
                msgs.append(e)
                msg = '预约号：{} 科室ID:{} 原因:{} 从体检系统获取科室项目失败'.format(order_id, department, repr(e))
                log.error(msg)
                log.exception(e)

    except NotFoundLisResultException as e:
        msgs.append(e)
        log.error(repr(e))
        log.exception(e)


    except TJException as e:
        msgs.append(e)
        msg = '传输预约号：{}时发生错误 原因:{}'.format(order_id, repr(e))
        log.error(msg)
        log.exception(e)

    # 更新param，直接指向一下个id
    if next_id is not None:
        log.info('开始保存下一个id:{}'.format(next_id))
        param = CurPosParams()
        param.save(int(next_id))

    return msgs


def trans_skdlis_by_assem(order_id, username, sex_name, age, department_id, assem_id, assem_name, items_list,
                          lis_result_dict):
    log.info('开始将项目列表转为map:{}'.format(items_list))
    items_dict = {}
    msgs = []
    for item in items_list:
        key = str(item['extSysCode'])
        if not key:
            msgs.append('项目id:{} 项目名称:{}没有有效的对照码'.format(item['itemId'], item['name']))
        else:
            maps = re.split(r',|，|\^|\|', key)
            for map in maps:
                items_dict[map] = item
    if len(msgs) > 0:
        raise TjAssemResultsException(order_id, username, sex_name, age, assem_id, assem_name, '\n'.join(msgs))

    set_keys = set(items_dict.keys()).intersection(set(lis_result_dict.keys()))

    log.info('获取到共有的项目信息:{}'.format(set_keys))

    reporter_id = None
    auditor_id = None

    if len(set_keys) > 0:
        lis_result = lis_result_dict[list(set_keys)[0]]
        try:
            reporter_id, auditor_id = _get_user_id(lis_result.OPERATOR_NAME, lis_result.AUDIT_NAME)
        except Exception as e:
            raise TjAssemResultsException(order_id, username, sex_name, age, assem_id, assem_name, repr(e))

    for key in set_keys:
        items_dict[key]['has_result'] = True

    save_lis_items = []

    for key in items_dict.keys():
        item = items_dict[key]
        if 'has_result' not in item.keys():
            msgs.append(
                '项目id:{} 项目名称:{} 对照码:{} 在lis中，没有找到对应的项目结果'.format(item['itemId'], item['name'], item['extSysCode']))
        else:
            _build_skd_lis(key,order_id,assem_id,save_lis_items, item, lis_result_dict[key], reporter_id, auditor_id)

    if len(msgs) > 0:
        raise TjAssemResultsException(order_id, username, sex_name, age, assem_id, assem_name, '\n'.join(msgs))

    try:
        r = tjAssert(save_lis(save_lis_items, department_id))
    except Exception as e:
        raise TjAssemResultsException(order_id, username, sex_name, age, assem_id, assem_name,
                                      '上传lis失败!{}'.format(repr(e)))

    log.info('保存lis成功[{}]'.format(r['msg']))


def _get_next_id(cur_id, lis_result_ids):
    if cur_id is not None:
        ids = [x for x in lis_result_ids if x > cur_id]
        ids.sort()
        l0 = len(ids) - 1
        if l0 == 0:
            return ids[0]
        while l0 > 0:
            if ids[l0] - ids[0] == l0:
                return ids[l0]
            l0 = l0 - 1
        return ids[0]
    else:
        return None


def _build_skd_lis(key, order_id, assem_id, save_lis_items, item, result_lis, reporter_id, auditor_id):
    item_dict = {
        'reserveId': order_id,
        'resultType': item['resultType'],
        'ferenceLowerLimit': item['ferenceLowerLimit'] if item['ferenceLowerLimit'] is not None else 0,
        'ferenceUpperLimit': item['ferenceUpperLimit'] if item['ferenceUpperLimit'] is not None else 0,
        'recvYsId': reporter_id if reporter_id is not None else auditor_id,
        'checkYsId': auditor_id if auditor_id is not None else reporter_id,
        'checkTjjg': result_lis.CONTENT_RESULT,
        'igId': assem_id,
        'itemId': item['itemId'],
        'reportingMark': '0'
    }
    save_lis_items.append(item_dict)


def _get_user_id(operator_name, audit_name):
    if (not operator_name) and (not audit_name):
        raise Exception('报告医生和审核医生不能同时为空')

    operator_id = None
    audit_id = None

    if operator_name:
        operator = tjAssert(get_user_info('lis', operator_name))
        operator_id = operator['msg']['userId']

    if audit_name:
        audit = tjAssert(get_user_info('lis', audit_name))
        audit_id = audit['msg']['userId']

    return operator_id, audit_id


def _loginTj():
    log.info('开始登录体检系统，用户名:{} 密码:{}'.format(SKD_TJ_NAME, SKD_TJ_PASSWORD))
    r = login(SKD_TJ_NAME, SKD_TJ_PASSWORD)
    tjAssert(r)
    log.info(r['msg'])
