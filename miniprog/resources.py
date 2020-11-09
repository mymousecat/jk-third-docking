# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     resources
   Description :
   Author :       wdh
   date：          2019/2/12
-------------------------------------------------
   Change Activity:
                   2019/2/12:
-------------------------------------------------
"""

from . import appconfig
from flask_restful import Resource, reqparse
import datetime
from .db_op import getPackages, \
    getPackageDetails, \
    getBasicInfo, \
    getOrderDigest, \
    getOrders, \
    getReportList, \
    getReportBasicInfo, \
    getReportSummaries, \
    getReportItemsResult, \
    getReportMainCheck, \
    getTeamOrderByCertId, \
    getTeamOrderDetail, \
    getOrderDigestByOrderId, \
    getReportListByOrderDate

from . import api, app
from flask import request, abort
from .models import MiniProgPackageDetails_
from .reporttemplate import ExamReportTemplate
from .teamtemplate import TeamOrderDetailsTemplate

import logging
from jktj.orders import OrderInfo, Orders
# from skdtj.skdtj import \
#     pay


from jktj.jktj import loginByUserNamePwd, \
    tjAssert, \
    saveOrder, \
    deleteOrder, \
    updateOrderDate, \
    pay

from werkzeug.exceptions import BadRequest, NotFound

log = logging.getLogger(__name__)

JK_EXAM_USERNAME = appconfig['JK_EXAM_USERNAME']
JK_EXAM_PASSWORD = appconfig['JK_EXAM_PASSWORD']

TJ_CUSTOMER_SOURCE = appconfig['TJ_CUSTOMER_SOURCE']


def _loginTj():
    log.info('开始登录体检系统...')
    r = loginByUserNamePwd(JK_EXAM_USERNAME, JK_EXAM_PASSWORD)
    tjAssert(r)
    log.info(r['msg'])


def _returnMessage(msg):
    r = {
        'message': {
        }
    }
    r['message'] = msg
    return r


class PackagesApi(Resource):
    def get(self, id=None):
        try:
            packTypeCode = request.args.get('packTypeCode', None)
            sexCode = request.args.get('sexCode', None)
            maritalCode = request.args.get('maritalCode', None)
            packages = getPackages(id=id, packTypeCode=packTypeCode, sexCode=sexCode, maritalCode=maritalCode)
            if (packages is None) or (isinstance(packages, list) and len(packages) == 0):
                abort(404, '没有找到符合条件的套餐!')
            else:
                return packages
        except Exception as e:
            dealException(e)


class PackageDetailsApi(Resource):
    def get(self, packageId):
        try:
            details = getPackageDetails(packageId)
            if (details is None) or (isinstance(details, list) and len(details) == 0):
                abort(404, '没有找到套餐ID为[{}]的明细信息!'.format(packageId))
            else:
                details_ = MiniProgPackageDetails_()
                for detail in details:
                    details_.addPackageDetails(detail)
                return details_.packageDetails_list
        except Exception as e:
            dealException(e)


# from utils import validator
# from utils import certtool

# from .validator import date,validCert,getInfo
from . import validator


def _checkAttr(d, attrName):
    if attrName not in d.keys():
        raise Exception('没有找到属性{}'.format(attrName))


def _verifyGroups(groups):
    _ATTRS = {'groupId', 'groupName', 'originalPrice', 'discountPrice', 'discountRate', 'departmentId'}
    for name in _ATTRS:
        _checkAttr(groups, name)
    return groups


def _getDateTime(strTime, isDayEnd):
    if strTime:
        t = datetime.datetime.strptime(strTime, '%Y-%m-%d')
        if isDayEnd:
            t = t + datetime.timedelta(days=1)
        return t
    else:
        return None


class OrdersApi(Resource):
    # def __init__(self):
    #     self.reqparse = reqparse.RequestParser()
    #     self.reqparse.add_argument('orderId', type=int,help='无效的预约号',location = 'values')
    #     self.reqparse = reqparse.RequestParser()
    #     self.reqparse.add_argument('username', type=str, required=True, help='用户名不能为空', location='json')
    #     self.reqparse.add_argument('mobile', type=str, required=True, help='手机号不能为空', location='json')
    #     self.reqparse.add_argument('maritalCode', type=str, help="婚姻状态编码必须在['1','2']内", choices=('1', '2'),
    #                                location='json')
    #     self.reqparse.add_argument('certId', type=validator.validCert, required=True, help="无效的身份证号", location='json')
    #     self.reqparse.add_argument('examType', type=str, help="体检类型必须在['01','03','04']内", choices=('01', '03', '04'),
    #                                default='01', location='json')
    #
    #     self.reqparse.add_argument('orderExamDate', type=validator.date, required=True, help="无效的预约日期", location='json')
    #
    #     self.reqparse.add_argument('packageId', type=str, default='', location='json')
    #
    #     self.reqparse.add_argument('subarea', required=True, type=str, help="分区代码必须在['1','2']内", choices=('1', '2'),
    #                                location='json')
    #
    #     self.reqparse.add_argument('groups', required=True, type=_verifyGroups, action='append', help='无效的项目组列表',
    #                                location='json')
    #
    #     super(OrdersApi, self).__init__()

    def _post_args(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('username', type=str, required=True, help='用户名不能为空', location='json')
        _reqparse.add_argument('mobile', type=str, required=True, help='手机号不能为空', location='json')
        _reqparse.add_argument('maritalCode', type=str, help="婚姻状态编码必须在['1','2']内", choices=('1', '2'),
                               location='json')
        _reqparse.add_argument('certId', type=validator.validCert, required=True, help="无效的身份证号", location='json')
        _reqparse.add_argument('examType', type=str, help="体检类型必须在['01','03','04']内", choices=('01', '03', '04'),
                               default='01', location='json')

        _reqparse.add_argument('orderExamDate', type=validator.date, required=True, help="无效的预约日期", location='json')

        _reqparse.add_argument('packageId', type=str, default='', location='json')

        # _reqparse.add_argument('subarea', required=True, type=str, help="分区代码必须在['1','2']内", choices=('1', '2'),
        #                        location='json')

        _reqparse.add_argument('groups', required=True, type=_verifyGroups, action='append', help='无效的项目组列表',
                               location='json')

        return _reqparse

    def post(self):
        """
        新建预约信息
        :return:
        """
        try:
            log.info('开始分析参数...')
            log.info('获取到预约参数:{}'.format(request.json))
            args = self._post_args().parse_args()
            certId = args.get('certId')
            log.info('开始查询身份证号为[{}]的人员基本信息...'.format(certId))
            basicInfo = getBasicInfo(certId)
            if basicInfo:
                log.info('查询到身份证:{} 的人员信息,姓名:{}  性别:{} 体检号:{}'.format(certId, basicInfo.username, basicInfo.sex,
                                                                      basicInfo.exam_no))
            else:
                log.info('没有查到身份证:{}的人员基本信息'.format(certId))

            log.info('开始解析身份证:{}的出生日期及性别...'.format(certId))
            certInfo = validator.getInfo(certId)
            log.info('从身份证获取的出身日期：{} 性别:{}'.format(certInfo['birth'], certInfo['sex']))

            if basicInfo is not None:
                personId = basicInfo.id
                log.info('根据人员信息id:{}获取未完成的（已预约）预约信息...'.format(personId))

                oInfo = getOrderDigest(personId)
                if oInfo:
                    abort(400, '您还有未完成的体检预约，预约号为[{}]，预约日期为:{}，请取消后此预约后再重新预约体检'.format(
                        oInfo.id,
                        oInfo.initial_time.strftime('%Y-%m-%d')
                    ))

            log.info('开始组装结果...')
            orderInfo = OrderInfo()
            orderInfo.addBasicInfo(username=args.get('username'),
                                   certId=args.get('certId'),
                                   birth=certInfo['birth'],
                                   sex=certInfo['sex'],
                                   mobile=args.get('mobile'),
                                   orderExamDate=args.get('orderExamDate'),
                                   examType=args.get('examType'),
                                   subarea=args.get('subarea'),
                                   customerSource=TJ_CUSTOMER_SOURCE,
                                   maritalStatus=args.get('maritalCode'),
                                   personId=basicInfo.id if basicInfo is not None else None,
                                   examNo=basicInfo.exam_no if basicInfo is not None else None,
                                   itemPackage=args.get('packageId')
                                   )
            groups = args.get('groups')
            for group in groups:
                orderInfo.addGroup(departmentId=group['departmentId'],
                                   groupId=group['groupId'],
                                   groupName=group['groupName'],
                                   originalPrice=group['originalPrice'],
                                   discountPrice=group['discountPrice'],
                                   discountRate=group['discountRate']
                                   )
            _loginTj()
            log.info('开始保存预约记录...')
            params = orderInfo.getParams()
            # log.info('预约信息:{}'.format(params))
            r = saveOrder(params)
            tjAssert(r)
            log.info('保存预约记录成功!')
            # (examNo, orderId) = r['msg'].split(',')
            return _returnMessage({
                'examNo': r['msg']['examNo'],
                'orderId': r['msg']['orderId']
            })
        except Exception as e:
            dealException(e)

    def delete(self, orderId):
        """
        删除预约号
        :param orderId:
        :return:
        """
        try:
            _loginTj()
            log.info('开始查询预约号为:{}的是否可删除'.format(orderId))
            r = getOrderDigestByOrderId(orderId)
            rowCount = len(r)
            log.info('获取到可删除的记录数为:{}'.format(rowCount))
            if rowCount == 0:
                abort(400, '不能删除本次预约，本预约不存在或已收费或正在体检')

            log.info('开始删除预约号为:{}的预约记录'.format(orderId))
            r = deleteOrder(orderId)
            tjAssert(r)
            log.info('删除预约号为:{}的预约记录成功'.format(orderId))
            return _returnMessage({
                'deletedOrderId': orderId
            })
            # return r
        except Exception as e:
            dealException(e)

    def get(self, certId):
        """
        根据身份证号，查找已预约记录
        :param certId:
        :return:
        """
        try:
            # 开始校验身份证
            try:
                validator.validCert(certId)
            except:
                abort(400, '{}为无效身份证'.format(certId))
            log.info('开始使用身份证:{}查询预约的记录...'.format(certId))
            orders = getOrders(certId)
            if isinstance(orders, list) and len(orders) == 0:
                abort(404, '没有找到身份证号为:{}的预约信息'.format(certId))

            o = Orders()
            for order in orders:
                o.addOrder(orderId=order.orderId,
                           examNo=order.examNo,
                           certId=order.certId,
                           username=order.username,
                           sexCode=order.sexCode,
                           sex=order.sex,
                           birth=order.birth,
                           age=order.age,
                           mobile=order.mobile,
                           customerSourceCode=order.customerSourceCode,
                           customerSource=order.customerSource,
                           examTypeCode=order.examTypeCode,
                           examType=order.examType,
                           maritalCode=order.maritalCode,
                           marital=order.marital,
                           examStatus=order.examStatus,
                           orderTime=order.orderTime,
                           examTime=order.examTime,
                           subareaCode=order.subareaCode,
                           subarea=order.subarea,
                           packageId=order.packageId,
                           packageName=order.packageName,
                           orderExamTime=order.orderExamTime
                           ).addGroup(departmentId=order.departmentId,
                                      departmentName=order.departmentName,
                                      departmentDisplayOrder=order.departmentDisplayOrder,
                                      groupId=order.groupId,
                                      groupName=order.groupName,
                                      groupDisplayOrder=order.groupDisplayOrder,
                                      clinicalSignificance=order.clinicalSignificance,
                                      originalPrice=order.originalPrice,
                                      discountPrice=order.discountPrice,
                                      discountRate=order.discountRate,
                                      feeType=order.feeType,
                                      costStatus=order.costStatus,
                                      completeStatus=order.completeStatus,
                                      completeTime=order.completeTime
                                      )

            return o.toDict()
        except Exception as e:
            dealException(e)


class ReportListCheckDateAPI(Resource):

    def _post_args(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('beginDate', type=validator.date, required=False, help="无效的起启日期", location='args')
        _reqparse.add_argument('endDate', type=validator.date, required=False, help="无效的终止日期", location='args')
        return _reqparse

    def get(self):
        """
        :param beginDate:
        :param enDate:
        :return:
        """
        try:
            args = self._post_args().parse_args()
            strBeginDate = args.get('beginDate')
            strEndDate = args.get('endDate')

            if (not strBeginDate) and (not strEndDate):
                abort(400, '请求参数beginDate及endDate不能全部为空')

            beginDate = _getDateTime(strBeginDate, False)
            endDate = _getDateTime(strEndDate, True)

            reportList = getReportListByOrderDate(beginDate, endDate)

            if not reportList:
                abort(404, '没有找到预约日期:{} 结束日期:{}日期内，已完成的报告'.format(
                    strBeginDate, strEndDate
                ))

            return reportList


        except Exception as e:
            dealException(e)


class ReportListAPI(Resource):
    def _post_args(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('beginDate', type=validator.date, required=False, help="无效的起启日期", location='args')
        _reqparse.add_argument('endDate', type=validator.date, required=False, help="无效的终止日期", location='args')
        return _reqparse

    def get(self, certId):
        """
        根据身份证号码，获取报告已完成的列表
        :param certId:
        :return:
        """
        try:

            # try:
            #     validator.validCert(certId)
            # except:
            #     abort(400, '{}为无效身份证'.format(certId))

            # 获取开始、结束日期参数
            args = self._post_args().parse_args()
            strBeginDate = args.get('beginDate')
            strEndDate = args.get('endDate')

            beginDate = _getDateTime(strBeginDate, False)
            endDate = _getDateTime(strEndDate, True)

            log.info('身份证号:{} 开始时间:{}  结束时间:{}'.format(certId, beginDate, endDate))
            reportList = getReportList(certId, beginDate, endDate)
            if isinstance(reportList, list) and len(reportList) == 0:
                abort(404, '没有找到身份证号为:{}的报告'.format(certId))
            return reportList
        except Exception as e:
            dealException(e)


class ReportAPI(Resource):

    def get(self, orderId):
        try:
            basicInfo = getReportBasicInfo(orderId)
            if basicInfo is None:
                abort(404, '没有找到预约号为:{}的体检报告'.format(orderId))
            examReport = ExamReportTemplate()
            examReport.buildCenterInfo(centerId='10001', centerName='上海长海医院体检中心')

            # 通讯信息
            if basicInfo.telephone:
                examReport.buildContactInfo(mobile=basicInfo.telephone,
                                            currentAddress=basicInfo.address,
                                            nativePlace=basicInfo.native_place,
                                            email=basicInfo.email
                                            )

            # 公司信息
            if basicInfo.org_id:
                examReport.buildCompanyInfo(companyName=basicInfo.org_name,
                                            companyId=basicInfo.org_id,
                                            contractId=basicInfo.contract_id,
                                            contractName=basicInfo.contract_name,
                                            department=basicInfo.departments,
                                            post=basicInfo.post,
                                            workNo=basicInfo.job_number
                                            )

            examReport.buildBasicInfo(persionId=basicInfo.exam_no,
                                      username=basicInfo.username,
                                      gender=basicInfo.gender,
                                      birth=basicInfo.birthday,
                                      nation=basicInfo.nation,
                                      certId=basicInfo.cert_id,
                                      created=basicInfo.initial_time,
                                      changed=basicInfo.change_time
                                      )

            examReport.buildOrderInfo(orderId=basicInfo.order_id,
                                      valid=True,
                                      opId=None,
                                      opName=None,
                                      age=basicInfo.age,
                                      examDate=basicInfo.arrival_date,
                                      examType=basicInfo.exam_type,
                                      orderStaff=basicInfo.order_staff,
                                      orderTime=basicInfo.order_initial_time,
                                      orderWay=basicInfo.customer_source,
                                      maritalStatus=basicInfo.marital_status,
                                      examTimes=basicInfo.exam_times
                                      )

            # 项目结果
            items = getReportItemsResult(orderId)
            examInfos = examReport.createExamInfos()
            for item in items:
                group = examInfos.addDepartment(departmentCode=item.department_id,
                                                departmentName=item.department_name,
                                                departmentType=item.deptclass,
                                                displayOrder=item.department_display_order
                                                ).addGroup(groupCode=item.assem_id,
                                                           groupName=item.assem_name,
                                                           displayOrder=item.assem_display_order,
                                                           groupType=item.assem_type,
                                                           giveup=item.assem_giveup
                                                           )
                ference = None
                if item.ference_lower_limit is not None and item.ference_upper_limit is not None and item.ference_upper_limit != item.ference_lower_limit:
                    ference = '{:.2f} - {:.2f}'.format(item.ference_lower_limit, item.ference_upper_limit)

                itemType = None
                if item.result_type == '1':
                    itemType = '数字'
                else:
                    itemType = '文本'

                flag = None
                if item.positive_symbol:
                    if item.positive_symbol.find('高') >= 0:
                        flag = '↑'
                    elif item.positive_symbol.find('低') >= 0:
                        flag = '↓'

                group.addItem(itemCode=item.element_id,
                              itemName=item.element_name,
                              itemResult=item.result_content,
                              itemType=itemType,
                              itemUnit=item.measurement_unit,
                              itemRef=ference,
                              flag=flag,
                              # ference_lower_limit
                              ferenceLowerLimit=None if item.ference_lower_limit is None else '{:.2f}'.format(
                                  item.ference_lower_limit),
                              # ference_upper_limit
                              ferenceUpperLimit=None if item.ference_upper_limit is None else '{:.2f}'.format(
                                  item.ference_upper_limit),
                              giveup=item.giveup_symbol
                              )
            # 项目组结论
            summaries = getReportSummaries(orderId)
            for summary in summaries:
                department = examInfos.addDepartment(departmentCode=summary.department_id,
                                                     departmentName=None
                                                     )
                if department is not None:
                    group = department.addGroup(groupCode=summary.element_assem_id,
                                                groupName=None
                                                )
                    if group is not None:
                        group.addSummary(summary=summary.merge_word,
                                         operatorId=summary.additional_operator_id,
                                         operatorName=summary.additional_operator_name,
                                         reportId=summary.operator_id,
                                         reportName=summary.operator_name,
                                         # 检查时间
                                         examTime=summary.complete_time,
                                         diseaseContent=summary.disease_content,
                                         selfWriteSymbol=summary.selfwrite_symbol,
                                         giveupSymbol='是' if summary.selfwrite_symbol == '04' else '否'
                                         )

            # 总检建议
            mainChecks = getReportMainCheck(orderId)
            for mainCheck in mainChecks:
                adviceInfos = examReport.createAdviceInfos(mainCheckDoctorId=mainCheck.main_check_uid,
                                                           mainCheckDoctorName=mainCheck.main_check_name,
                                                           mainCheckTime=mainCheck.main_check_date,
                                                           finalCheckDoctorId=mainCheck.final_check_uid,
                                                           finalCheckDoctorName=mainCheck.final_check_name,
                                                           finalCheckTime=mainCheck.final_check_date,
                                                           earlyCheckDoctorId=mainCheck.early_check_uid,
                                                           earlyCheckDoctorName=mainCheck.early_check_name,
                                                           earlyCheckTime=mainCheck.early_check_date
                                                           )
                adviceInfos.addAdvise(diseaseName=mainCheck.merge_word, diseaseAdvice=mainCheck.recommend,
                                      diseaseId=mainCheck.disease_id)

            return examReport.examReport

        except Exception as e:
            dealException(e)


class TeamApi(Resource):

    def get(self, certId):
        try:
            # 校验身份证号
            try:
                validator.validCert(certId)
            except:
                abort(400, '{}为无效身份证'.format(certId))

            orderInfo = getTeamOrderByCertId(certId)
            if orderInfo is None:
                abort(404, '未发现身份证号为:{}的团检预约信息'.format(certId))

            template = TeamOrderDetailsTemplate()

            orderDetails = getTeamOrderDetail(orderInfo.order_id)

            if len(orderDetails) == 0:
                abort(404, '未发现身份证号为:{}的团检预约信息'.format(certId))

            for detail in orderDetails:
                template.addBasicInfo(
                    orderId=detail.order_id,
                    examStatus=detail.exam_status,
                    orderExamDate=detail.order_exam_date,
                    age=detail.age,
                    subareaCode=detail.subarea_code,
                    subarea=detail.subarea,
                    examNo=detail.exam_no,
                    certId=detail.cert_id,
                    username=detail.username,
                    sexCode=detail.sex_code,
                    sex=detail.sex,
                    birth=detail.birthday,
                    telephone=detail.telephone,
                    companyId=detail.company_id,
                    companyName=detail.company_name,
                    examBeginDate=detail.exam_begin_date,
                    examEndDate=detail.exam_end_date
                )

                template.addGroup(departmentId=detail.department_id,
                                  departmentName=detail.department_name,
                                  departmentDisplayOrder=detail.department_display_order,
                                  groupId=detail.assem_id,
                                  groupName=detail.assem_name,
                                  groupDisplayOrder=detail.com_display_order,
                                  clinicalSignificance=detail.clinical_significance,
                                  attention=detail.guidelines_single_prompt
                                  )

            return template.teamOrderDtails


        except Exception as e:
            dealException(e)

    def _post_args(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('orderId', type=int, required=True, help='预约号不能为空', location='json')
        _reqparse.add_argument('orderExamDate', type=validator.date, nullable=True, required=True,
                               help='无效的预约日期', location='json')
        return _reqparse

    def put(self):
        try:
            args = self._post_args().parse_args()
            log.info('开始改修团检的日期...')
            _loginTj()
            r = updateOrderDate(
                orderId=args.get('orderId'),
                orderExamDate=args.get('orderExamDate')
            )
            log.info(r)
            tjAssert(r)
            return _returnMessage({
                'success': True
            })
        except Exception as e:
            dealException(e)


class PaymentApi(Resource):
    def _post_args(self):
        _reqparse = reqparse.RequestParser()
        _reqparse.add_argument('orderId', type=int, required=True, help='预约号不能为空', location='json')
        _reqparse.add_argument('paymentAmount', type=float, required=True, help='无效的支付金额', location='json')
        _reqparse.add_argument('payId', type=str, required=True, help='无效的支付ID', location='json')
        _reqparse.add_argument('payGroupIds', type=int, action='append', required=True, help='无效的待支付项目组列表',
                               location='json')
        _reqparse.add_argument('payType', type=str, required=True, choices=('ZFB', 'WX'), help='无效的支付类型,必须指定WX或ZFB',
                               location='json')
        return _reqparse

    def post(self):
        try:
            args = self._post_args().parse_args()
            orderId = args.get('orderId')
            paymentAmount = args.get('paymentAmount')
            payId = args.get('payId')
            payGroupIds = args.get('payGroupIds')
            pt = args.get('payType')

            payType = None
            if pt == 'WX':
                payType = '微信'
            elif pt == 'ZFB':
                payType = '支付宝'

            log.info(
                '收到支付命令，参数为orderId:{} paymentAmount:{} payId:{} payGroupdIds:{} '.format(orderId, paymentAmount, payId,
                                                                                         payGroupIds))

            # 开始登录体检
            _loginTj()

            r = pay(orderId=orderId, paymentAmount=paymentAmount, payGroupIds=payGroupIds, payId=payId, payType=payType)

            log.info('支付完成后，获取返回。{}'.format(r))

            tjAssert(r)

            return r

        except Exception as e:
            dealException(e)


def dealException(e):
    if isinstance(e, BadRequest):
        raise e
    elif isinstance(e, NotFound):
        raise e
    else:
        abort(500, repr(e))


api.add_resource(PackagesApi,
                 '/api/v1.0/packages',
                 '/api/v1.0/packages/<int:id>',
                 endpoint='packages')

api.add_resource(PackageDetailsApi,
                 '/api/v1.0/packageDetails/<int:packageId>',
                 endpoint='packageDetails')

api.add_resource(OrdersApi,
                 '/api/v1.0/orders',
                 '/api/v1.0/orders/<int:orderId>',
                 '/api/v1.0/orders/certId/<string:certId>',
                 endpoint='orders')

api.add_resource(ReportListAPI,
                 '/api/v1.0/reports/certId/<string:certId>',
                 endpoint='reports'
                 )

api.add_resource(ReportListCheckDateAPI,
                 '/api/v1.0/reports/orderCheckDate',
                 endpoint='reports_checkdate'
                 )

api.add_resource(ReportAPI,
                 '/api/v1.0/report/<int:orderId>',
                 endpoint='report'
                 )

api.add_resource(TeamApi,
                 '/api/v1.0/team/certId/<string:certId>',
                 '/api/v1.0/team',
                 endpoint='team'
                 )

api.add_resource(PaymentApi,
                 '/api/v1.0/payment',
                 endpoint='payment'
                 )
