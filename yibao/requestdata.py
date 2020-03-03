# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     requestdata
   Description :
   Author :       wdh
   date：          2019/7/15
-------------------------------------------------
   Change Activity:
                   2019/7/15:
-------------------------------------------------
"""

import lxml.html
from .xml_util import getElement, addElement, addElementByNode
from .util import get_msg_id
import logging

et = lxml.html.etree

log = logging.getLogger(__name__)


class ExaminationResult:

    def __init__(self, examination_result_xml):
        self._xml = examination_result_xml

    def _create_node(self, parent, node_name, node_value):
        e = et.SubElement(parent, node_name)
        e.text = str(node_value) if node_value is not None else None

    def _add_group(self, group_code, group_name, dept_no, dept_name, check_result, check_doc, check_date):
        """
        增加项目组，就是分类
        :param group_code:
        :param group_name:
        :param dept_no:
        :param dept_name:
        :param check_result:
        :param check_doc:
        :param check_date:
        :return:
        """
        group_name_node = self._xml.xpath('//ITEMGROUP[ITEMGROUPCODE="{}"]'.format(group_code))
        group_node = None
        if len(group_name_node) == 0:
            # 创建
            group_node = et.SubElement(self._xml, 'ITEMGROUP')
            self._create_node(group_node, 'ITEMGROUPCODE', group_code)
            self._create_node(group_node, 'ITEMGROUPNAME', group_name)
            self._create_node(group_node, 'DEPTNO', dept_no)
            self._create_node(group_node, 'DEPTNAME', dept_name)
            self._create_node(group_node, 'CHECKRESULT', check_result)
            self._create_node(group_node, 'CHECKDOC', check_doc)
            self._create_node(group_node, 'CHECKDATE', check_date)
        else:
            group_node = group_name_node[0]
        return group_node

    def _add_item(self, group_node, item_code, item_name, doppler_part, lxd_part, dept_no, dept_name, result_value,
                  result_type,
                  structure_result, describe_code, min_value, max_value, unit, check_result, check_doc, input_doc,
                  check_date):
        item_node = et.SubElement(group_node, 'ITEM')
        self._create_node(item_node, 'ITEMCODE', item_code)
        self._create_node(item_node, 'ITEMNAME', item_name)
        self._create_node(item_node, 'DOPPLERPART', doppler_part)
        self._create_node(item_node, 'LXDPART', lxd_part)
        self._create_node(item_node, 'DEPTNO', dept_no)
        self._create_node(item_node, 'DEPTNAME', dept_name)
        self._create_node(item_node, 'RESULTVALUE', result_value)
        self._create_node(item_node, 'RESULTTYPE', result_type)
        self._create_node(item_node, 'STRUCTURERESULT', structure_result)
        self._create_node(item_node, 'DESCRIBECODE', describe_code)
        self._create_node(item_node, 'MINVALUE', min_value)
        self._create_node(item_node, 'MAXVALUE', max_value)
        self._create_node(item_node, 'UNIT', unit)
        self._create_node(item_node, 'CHECKRESULT', check_result)
        self._create_node(item_node, 'CHECKDOC', check_doc)
        self._create_node(item_node, 'INPUTDOC', input_doc)
        self._create_node(item_node, 'CHECKDATE', check_date)
        return item_node

    def addPhoto(self, group_node, item_code, item_name, result_value, check_doc, check_date, photo_type, photo_code):
        item_node_list = group_node.xpath('//ITEM[ITEMCODE="{}"]'.format(item_code))
        item_node = None
        if len(item_node_list) == 0:
            item_node = self._add_item(group_node, item_code, item_name, None, None, None, None, result_value, '2',
                                       None, None, None, None, None, None, check_doc, None, check_date)
        else:
            item_node = item_node_list[0]

        photo_node = et.SubElement(item_node, 'PHOTO')

        photo_type_node = et.SubElement(photo_node, 'PHOTOTYPE')
        photo_type_node.text = photo_type

        photo_code_node = et.SubElement(photo_node, 'PHOTOCODE')
        photo_code_node.text = photo_code

    def _addCover(self, item_code, item_name, item_value, check_date):
        """
        封面
        :param item_code:
        :param item_name:
        :param item_value:
        :param check_date:
        :return:
        """
        group_node = self._add_group('RC0001', '体检封面', None, None, None, None, check_date)
        # 开始创建小项
        self._add_item(group_node=group_node,
                       item_code=item_code,
                       item_name=item_name,
                       doppler_part=None,
                       lxd_part=None,
                       dept_no=None,
                       dept_name=None,
                       result_value=item_value,
                       result_type='2',
                       structure_result=None,
                       describe_code=None,
                       min_value=None,
                       max_value=None,
                       unit=None,
                       check_result=None,
                       check_doc=None,
                       input_doc=None,
                       check_date=check_date

                       )
        return self

    def setCheckDoc(self, group_node, doctor):
        e = group_node.xpath('CHECKDOC')
        if len(e) > 0:
            e[0].text = doctor

    def setCheckResult(self, group_node, check_result):
        e = group_node.xpath('CHECKRESULT')
        if len(e) > 0:
            e[0].text = check_result

    def addGroup(self, group_code, group_name, dept_no, dept_name, check_result, check_doc, check_date):
        return self._add_group(group_code, group_name, dept_no, dept_name, check_result, check_doc, check_date)

    def addItemResult(self, group_node, item_code, item_name,
                      doppler_part, lxd_part, result_value,
                      result_type,
                      structure_result, describe_code, min_value, max_value, unit, item_check_result, item_check_doc,
                      input_doc,
                      check_date):

        self._add_item(group_node, item_code, item_name, doppler_part, lxd_part, None, None, result_value,
                       result_type,
                       structure_result, describe_code, min_value, max_value, unit, item_check_result, item_check_doc,
                       input_doc, check_date)

    def addCoverHospName(self, hosp_name, check_date):
        """
        封面-医院名字
        :param hosp_name:
        :return:
        """
        return self._addCover('RC0001001', '医院名称', hosp_name, check_date)

    def addCoverHospAddr(self, hosp_addr, check_date):
        """
        封面-医院地址
        :param hosp_name:
        :return:
        """
        return self._addCover('RC0001002', '医院地址', hosp_addr, check_date)
        return self

    def addCoverHospTel(self, hosp_tel, check_date):
        """
        封面-联系电话
        :param hosp_tel:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001003', '联系电话', hosp_tel, check_date)
        return self

    def addCoverHospWeb(self, hosp_web, check_date):
        """
        封面-官网地址
        :param hosp_web:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001004', '医院官网', hosp_web, check_date)
        return self

    def addCoverHospLogo(self, hosp_logo, check_date):
        """
        封面-医院logo
        :param hosp_log:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001005', '医院LOGO', hosp_logo, check_date)
        return self

    def addCoverHospComplaintTel(self, hosp_complaint_tel, check_date):
        """
        封面-医院投诉电话
        :param hosp_complaint_tel:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001006', '投诉电话', hosp_complaint_tel, check_date)
        return self

    def addCoverHospGreeting(self, hosp_greeting, check_date):
        """
        封面-医院对体检人员致辞
        :param hosp_greeting:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001007', '医院对体检人员致辞', hosp_greeting, check_date)
        return self

    def addCoverHospZone(self, hosp_zone, check_date):
        """
        封面-统筹区
        :param hosp_greeting:
        :param check_date:
        :return:
        """
        return self._addCover('RC0001008', '统筹区', hosp_zone, check_date)
        return self


class RequestInputData:
    def __init__(self, xmlnode):
        self._xmlnode = xmlnode

    def addOrderId(self, order_id):
        """
        医疗机构体检编号
        :param order_id:
        :return:
        """
        addElementByNode(self._xmlnode, 'AHE002', order_id)
        return self

    def addYiBao(self, yibao_id):
        """
        个人医保编号
        :param yibao_id:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAC001', yibao_id)
        return self

    def addName(self, username):
        """
        姓名
        :param username:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAC003', username)
        return self

    def addSexCode(self, sex_code):
        """
        性别编码
        :param sex_code:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAC004', sex_code)
        return self

    def addIdCard(self, id_card):
        """
        身份证
        :param id_card:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAE135', id_card)
        return self

    def addUserType(self, user_type):
        """
        人员类别
        :param user_type:
        :return:
        """
        addElementByNode(self._xmlnode, 'AKC021', user_type)
        return self

    def addAge(self, age):
        """
        年龄
        :param age:
        :return:
        """
        addElementByNode(self._xmlnode, 'AKC023', age)
        return self

    def addCardNo(self, card_no):
        """
        卡号
        :param card_no:
        :return:
        """
        addElementByNode(self._xmlnode, 'AKC020', card_no, False)
        return self

    def addMobile(self, mobile):
        """
        联系电话
        :param mobile:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAE005', mobile)
        return self

    def addCompanyId(self, company_id):
        """
        单位编号
        :param companyId:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAB001', company_id)
        return self

    def addCompanyName(self, company_name):
        """
        单位编号
        :param company_name:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAB004', company_name)
        return self

    def addWorkno(self, workno):
        """
        工号
        :param workno:
        :return:
        """
        addElementByNode(self._xmlnode, 'WORKNO', workno, False)
        return self

    def addExamDate(self, exam_date):
        """
        体检日期
        :param exam_date:
        :return:
        """
        addElementByNode(self._xmlnode, 'EXAMINEDATE', exam_date)
        return self

    def addFinalResult(self, final_result):
        """
        终检结论
        :param final_result:
        :return:
        """
        addElementByNode(self._xmlnode, 'FINALRESULT', final_result, False)
        return self

    def addFinalDoctor(self, final_doctor):
        """
        终检医师
        :param final_doctor:
        :return:
        """
        addElementByNode(self._xmlnode, 'FINALDOCTOR', final_doctor)
        return self

    def addHealthAdvice(self, health_advice):
        """
        终检建议
        :param health_advice:
        :return:
        """
        addElementByNode(self._xmlnode, 'HEALTHADVICE', health_advice, False)
        return self

    def addOrgAmount(self, org_amount):
        """
        中心金额
        :param org_amount:
        :return:
        """
        addElementByNode(self._xmlnode, 'AHC002', org_amount, False)
        return self

    def addCompanyAmount(self, company_amount):
        """
        单位金额
        :param company_amount:
        :return:
        """
        addElementByNode(self._xmlnode, 'AHC003', company_amount, False)
        return self

    def addPersonalAmount(self, personal_amount):
        """
        个人金额
        :param personal_amount:
        :return:
        """
        addElementByNode(self._xmlnode, 'AHC004', personal_amount, False)
        return self

    def addExamYear(self, exam_year):
        """
        体检年度
        :param exam_year:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAE001', exam_year)
        return self

    def addZone(self, zone):
        """
        所属统筹区域
        :param zone:
        :return:
        """
        addElementByNode(self._xmlnode, 'AAB034', zone)
        return self

    def buildExamnationResult(self):
        exam_result_xml_node = addElementByNode(self._xmlnode, 'EXAMINATIONRESULT', None, False)
        return ExaminationResult(exam_result_xml_node)


class RequestData:
    def __init__(self, hosp_id, hosp_name, msg_no, grant_id, oper_id, oper_name):
        self._xml = """
            <YBJKDATA><REQUESTDATA></REQUESTDATA></YBJKDATA> 
        """
        self._xml_doc = et.fromstring(self._xml)
        node = getElement(self._xml_doc, '/YBJKDATA/REQUESTDATA')
        addElementByNode(node, 'AKB020', hosp_id)
        addElementByNode(node, 'AKB021', hosp_name)
        addElementByNode(node, 'MSGNO', msg_no)
        addElementByNode(node, 'MSGID', get_msg_id(hosp_id))
        addElementByNode(node, 'GRANTID', grant_id)
        addElementByNode(node, 'OPERID', oper_id)
        addElementByNode(node, 'OPERNAME', oper_name)
        self._inputnode = addElementByNode(node, 'INPUT', None, False)

    def buildInput(self):
        return RequestInputData(self._inputnode)

    def tostring(self):
        return str(et.tostring(self._xml_doc, xml_declaration=True, pretty_print=True, encoding='UTF-8'),
                   encoding='utf-8')
