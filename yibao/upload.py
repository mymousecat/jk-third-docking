# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     upload
   Description :
   Author :       wdh
   date：          2019/7/17
-------------------------------------------------
   Change Activity:
                   2019/7/17:
-------------------------------------------------
"""

from . import appconfig
import logging
import re
from .db_op import get_basicinfo, get_recheck, get_summary, get_element_result, get_image_dict
from .webserviceclient import get_info_from_yibao, buildRequestData, upload_exam
from .downloadfile import download_image
from .err import NotFoundException, InValidException

log = logging.getLogger(__name__)


# 测试数据
# 315471	2	颜小丹	460027199302254126	26	13876190314


def _get_summaries(summries):
    """
    获取结论
    :param summries:
    :return:
    """
    disease_list = []
    default_list = []
    giveup_list = []
    for summary in summries:
        if summary.selfwrite_symbol in ['01', '02']:
            disease_list.append(summary.merge_word)
        elif summary.selfwrite_symbol == '03':
            default_list.append('未见明显异常')
        elif summary.selfwrite_symbol == '04':
            giveup_list.append('自愿放弃')

    if len(disease_list) > 0:
        return set(disease_list)
    elif len(default_list) > 0:
        return set(default_list)
    elif len(giveup_list) > 0:
        return set(giveup_list)


def upload(order_id):
    """
    体检数据上传
    :param order_id:
    :return:
    """
    log.info('开始从体检系统中，获取预约号为：{}的体检人员基本信息...'.format(order_id))
    basicinfo = get_basicinfo(order_id)
    if not basicinfo:
        raise NotFoundException('预约号为:{}在体检系统中，没有找到'.format(order_id))

    log.info('获取预约号为:{}的基本信息,姓名:{} 身份证号:{} 性别:{} 年龄:{} 电话:{} 工号:{} 报道日期:{}'.format(
        order_id, basicinfo.username, basicinfo.cert_id, basicinfo.sex, basicinfo.age, basicinfo.telephone,
        basicinfo.job_number, basicinfo.arrival_date
    ))

    if not basicinfo.cert_id:
        raise InValidException('预约号为:{}的身份证号无效'.format(order_id))

    # 检查日期
    check_date = basicinfo.arrival_date.strftime('%Y-%m-%d')
    age = basicinfo.age
    main_check_doctor = basicinfo.main_check_doctor
    log.info('获取到检查日期(报道日期):{} 年龄:{} 主检医生:{}'.format(check_date, age, main_check_doctor))

    cert_id = basicinfo.cert_id.upper().strip()
    username = basicinfo.username.strip()

    # cert_id = '130103198603069019'
    # username = '吴天'

    log.info('开始使用姓名：{} 身份证号:{} 参数，在医保系统中进行查询信息....'.format(basicinfo.username, cert_id))
    response = get_info_from_yibao(username, cert_id)
    yb_hao = response['AAC001']  # 医保号
    username = response['AAC003']
    sex = response['AAC004']  # 性别编码
    card_no = response['AKC020']  # 卡号
    user_type = response['AKC021']  # 人员类别
    telephone = response['AAE005']  # 联系电话
    company_id = response['AAB001']  # 单位编号
    company_name = response['AAB004']  # 单位名称
    zone = response['AAB034']

    log.info(
        '获取到医保信息\nyb_hao:{}\nusername:{}\nsex:{}\ncard_no:{}\nuser_type:{}\ntelephone:{}\ncompany_id:{}\ncompany_name:{}'.format(
            yb_hao,
            username,
            sex,
            card_no,
            user_type,
            telephone,
            company_id,
            company_name
        ))

    log.info('开始获取主检建议...')
    recheck_list = get_recheck(order_id)
    disease_list = []
    advice_list = []
    for recheck in recheck_list:
        disease_list.append(recheck.merge_word)
        advice_list.append('【{}】\n{}'.format(recheck.merge_word, recheck.recommend))

    str_disease = '\n'.join(disease_list)
    str_advice = '\n'.join(advice_list)

    log.info('获取到疾病列表:{}'.format(str_disease))
    log.info('获取到建议列表:{}'.format(str_advice))

    log.info('开始查询项目组结论信息...')
    summary_dict = get_summary(order_id)
    log.info('获取到项目组结论信息:{}'.format(summary_dict))
    log.info('开始获取项目结果信息...')
    result_list = get_element_result(order_id)
    log.info('共获取到{}条项目结果'.format(result_list))

    log.info('开始获取报告图像信息...')
    image_count, images_dict = get_image_dict(order_id)
    log.info('总共获取到:{}张图像'.format(image_count))

    log.info('*****************************************************************************')
    log.info('开始组装上传字符串...')
    request_data = buildRequestData('BI411001')
    input = request_data.buildInput()
    examnationResult = input.addOrderId(order_id).addYiBao(yb_hao).addName(username).addSexCode(sex).addIdCard(
        cert_id).addAge(
        age).addCardNo(card_no).addUserType(user_type).addMobile(
        telephone if telephone else basicinfo.telephone).addCompanyId(company_id).addCompanyName(
        company_name).addWorkno(basicinfo.job_number).addExamDate(check_date).addFinalResult(
        str_disease).addHealthAdvice(str_advice).addFinalDoctor(main_check_doctor).addCompanyAmount(
        0).addPersonalAmount(0).addOrgAmount(0).addExamYear(appconfig['EXAM_YEAR']).addZone(
        zone).buildExamnationResult()

    examnationResult.addCoverHospName(appconfig['HOSP_NAME'], check_date). \
        addCoverHospAddr(appconfig['HOSP_ADDR'], check_date). \
        addCoverHospTel(appconfig['HOSP_TEL'], check_date). \
        addCoverHospWeb(appconfig['HOSP_WEB'], check_date). \
        addCoverHospLogo(appconfig['HOSP_LOGO'], check_date). \
        addCoverHospComplaintTel(appconfig['HOSP_COMPLAINT_TEL'], check_date). \
        addCoverHospGreeting(appconfig['HOSP_GREETING'], check_date). \
        addCoverHospZone(appconfig['HOSP_ZONE_NAME'], check_date)

    log.info('开始分析项目结果...')

    yb_describle_dict = {}
    yb_summary_dict = {}
    yb_report_dict = {}

    # 项目组名称子典
    assem_name_dict = {}

    for result in result_list:

        assem_name_dict[str(result.assem_id)] = result.assem_name

        if not result.map_code:
            log.log('项目组id:{} 项目组名称:{} 项目id:{} 项目名称:{} 的MAP_CODE为空，将忽略上传'.format(result.assem_id, result.assem_name,
                                                                                     result.element_id,
                                                                                     result.element_name))
            continue

        log.info('获取到项目id:{} 项目名称:{}的MAP_CODE:{}'.format(result.element_id, result.element_name, result.map_code))

        codes = re.split(r'\|', result.map_code)
        if len(codes) != 9:
            raise InValidException(
                '项目id:{} 项目名称:{} 中存在无效的MAP_CODE:{}'.format(result.element_id, result.element_name, result.map_code))

        log.info('分析后的codes:{}'.format(codes))

        yb_group_id = codes[0]
        yb_group_name = codes[1]
        yb_element_id = codes[2]
        yb_element_name = codes[3]
        yb_bc_part = codes[4]
        yb_lxd_part = codes[5]
        yb_describle = codes[6]  # 检查描述
        yb_dialog = codes[7]  # 检查印象
        yb_report = codes[8]  # 检查报告

        log.info('获取项目组小结...')
        key = str(result.assem_id)
        summaries = summary_dict[key]
        summary_list = []
        yibao_disease_list_tmp = []
        for summary in summaries:
            summary_list.append(summary.merge_word)
            if summary.map_code:
                yibao_disease_list_tmp.append(summary.map_code)
        str_summaries = '\n'.join(summary_list)
        log.info('获取到结论列表:{}'.format(str_summaries))

        yb_disease = []
        for t1 in yibao_disease_list_tmp:
            t2 = re.split(r',', t1)
            for t3 in t2:
                t4 = re.split(r'\|', t3)
                if len(t4) == 1:
                    yb_disease.append(t4[0])
                elif len(t4) == 2 and t4[0] == yb_group_id:
                    yb_disease.append(t4[1])
        str_yb_disease = '|'.join(yb_disease)

        log.info('获取到医保疾病列表:{}'.format(str_yb_disease))

        group_node = examnationResult.addGroup(
            group_code=yb_group_id,
            group_name=yb_group_name,
            dept_no=result.department_id,
            dept_name=result.department_name,
            check_result=str_summaries,
            check_doc=result.doc_name,
            check_date=check_date
        )

        if yb_element_id:
            examnationResult.addItemResult(
                group_node=group_node,
                item_code=yb_element_id,
                item_name=yb_element_name,
                doppler_part=yb_bc_part,
                lxd_part=yb_lxd_part,
                result_value=result.result_content,
                result_type=result.result_type,
                structure_result=str_yb_disease if str_yb_disease else '0',
                describe_code=999,
                min_value='%.1f' % result.low if result.low is not None else None,
                max_value='%.1f' % result.upper if result.upper is not None else None,
                unit=result.unit,
                item_check_result=None,
                item_check_doc=result.doc_name,
                input_doc=result.addop_name,
                check_date=check_date
            )

        if yb_describle:  # 如果存在描述代码
            if yb_group_id not in yb_describle_dict.keys():
                yb_describle_dict[yb_group_id] = {
                    'element_name': '检查描述',
                    'item_check_doc': [],
                    'check_date': check_date,
                    'desc': [],
                    'element_id': yb_describle,
                    'disease_list': []
                }
            yb_describle_dict[yb_group_id]['desc'].append(result.result_content)
            yb_describle_dict[yb_group_id]['item_check_doc'].append(result.doc_name)
            yb_describle_dict[yb_group_id]['disease_list'].extend(yb_disease)

        if yb_dialog:  # 如果存在检查印象代码
            if yb_group_id not in yb_summary_dict.keys():
                yb_summary_dict[yb_group_id] = {
                    'element_name': '检查印象' if yb_dialog != 'RC0006003' else '裂隙灯检查汇总描述',
                    'item_check_doc': [],
                    'check_date': check_date,
                    'summaries': [],
                    'element_id': yb_dialog,
                    'disease_list': []
                }
            yb_summary_dict[yb_group_id]['summaries'].extend(summaries)
            yb_summary_dict[yb_group_id]['item_check_doc'].append(result.doc_name)
            yb_summary_dict[yb_group_id]['disease_list'].extend(yb_disease)

        if yb_report:  # 如果存在检查报告代码
            if yb_group_id not in yb_report_dict.keys():
                yb_report_dict[yb_group_id] = {
                    'element_name': '检查报告',
                    'item_check_doc': [],
                    'check_date': check_date,
                    'element_assem_ids': [],
                    'element_assem_names': [],
                    'element_id': yb_report
                }
            yb_report_dict[yb_group_id]['element_assem_ids'].append(result.assem_id)
            yb_report_dict[yb_group_id]['element_assem_names'].append(result.assem_name)
            yb_report_dict[yb_group_id]['item_check_doc'].append(result.doc_name)

    log.info('开始增加检查描述...')
    for group_id in yb_describle_dict.keys():
        group_node = examnationResult.addGroup(
            group_code=group_id,
            group_name=None,
            dept_no=None,
            dept_name=None,
            check_result=None,
            check_doc=None,
            check_date=None
        )

        set_disease = set(yb_describle_dict[group_id]['disease_list'])

        examnationResult.addItemResult(
            group_node=group_node,
            item_code=yb_describle_dict[group_id]['element_id'],
            item_name=yb_describle_dict[group_id]['element_name'],
            doppler_part=None,
            lxd_part=None,
            result_value='\n'.join(yb_describle_dict[group_id]['desc']),
            result_type=2,
            structure_result='|'.join(set_disease) if len(set_disease) > 0 else '0',
            describe_code='999',
            min_value=None,
            max_value=None,
            unit=None,
            item_check_result=None,
            item_check_doc='|'.join(set(yb_describle_dict[group_id]['item_check_doc'])),
            input_doc=None,
            check_date=check_date
        )

    log.info('开始增加检查印象...')
    for group_id in yb_summary_dict.keys():
        group_node = examnationResult.addGroup(
            group_code=group_id,
            group_name=None,
            dept_no=None,
            dept_name=None,
            check_result=None,
            check_doc=None,
            check_date=None
        )

        # for summary in yb_summary_dict[group_id]['summaries']:
        #     log.warning('医保项目组:{} 结论类型:{} 获取的结论:{}'.format(group_id, summary.selfwrite_symbol, summary.merge_word))

        summaries = '\n'.join(_get_summaries(yb_summary_dict[group_id]['summaries']))

        item_check_doc = '|'.join(set(yb_summary_dict[group_id]['item_check_doc']))

        set_disease = set(yb_summary_dict[group_id]['disease_list'])

        examnationResult.addItemResult(
            group_node=group_node,
            item_code=yb_summary_dict[group_id]['element_id'],
            item_name=yb_summary_dict[group_id]['element_name'],
            doppler_part=None,
            lxd_part=None,
            result_value=summaries,
            result_type=2,
            structure_result='|'.join(set_disease) if len(set_disease) > 0 else '0',
            describe_code='999',
            min_value=None,
            max_value=None,
            unit=None,
            item_check_result=None,
            item_check_doc=item_check_doc,
            input_doc=None,
            check_date=check_date
        )

        # log.warning('医保项目组id:{}  结论:{}'.format(group_id, summaries))
        examnationResult.setCheckDoc(group_node, item_check_doc)
        examnationResult.setCheckResult(group_node, summaries)

    log.info('开始增加检查报告...')
    for group_id in yb_report_dict.keys():
        group_node = examnationResult.addGroup(
            group_code=group_id,
            group_name=None,
            dept_no=None,
            dept_name=None,
            check_result=None,
            check_doc=None,
            check_date=None
        )

        log.info('获取含有图像的项目组...')
        # photo_assem_names = []
        photo_assem_medias = []
        log.log('开始检查项目组列表:{}中的图像'.format(yb_report_dict[group_id]['element_assem_ids']))

        for assem_id in yb_report_dict[group_id]['element_assem_ids']:
            key = str(assem_id)
            if key in images_dict.keys():
                photo_assem_medias.extend(images_dict[key])

        set_photo_assem_medias = set(photo_assem_medias)

        log.log(set_photo_assem_medias)

        log.log('开始下载图像...')
        set_assem_name = set()
        photo_list = []
        for media in set_photo_assem_medias:
            try:
                media_type, content = download_image(media)
                key = str(media.element_assem_id)
                assem_name = assem_name_dict[key]
                set_assem_name.add(assem_name)
                photo_list.append(
                    {
                        'media_type': media_type,
                        'content': content
                    }
                )
            except Exception as e:
                log.error('下载图像失败!预约号:{} 项目组id:{}'.format(media.order_id, media.element_assem_id))
                log.exception(e)

        # 开启增加图像功能
        for photo in photo_list:
            examnationResult.addPhoto(group_node=group_node,
                                      item_code=yb_report_dict[group_id]['element_id'],
                                      item_name=yb_report_dict[group_id]['element_name'],
                                      result_value=','.join(set_assem_name),
                                      check_doc=','.join(set(yb_report_dict[group_id]['item_check_doc'])),
                                      check_date=check_date,
                                      photo_type=photo['media_type'],
                                      photo_code=photo['content']
                                      )

    response = upload_exam(request_data)
    log.log('响应结果:{}'.format(response))
