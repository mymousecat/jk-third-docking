# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     db_op
   Description :
   Author :       wdh
   date：          2019/2/12
-------------------------------------------------
   Change Activity:
                   2019/2/12:
-------------------------------------------------
"""

from . import getSession
from .models import MiniProgPackages, \
    MiniProgPackageDetails, \
    MiniProgBaseInfo, \
    MiniProgOrderDigest, \
    MiniProgOrders, \
    MiniProgReportList, MiniProgBasicInfo, MiniProgItemResults, MiniProgSummaries, MiniProgMainCheck, \
    MiniProgTeamOrder, MiniProgTeamOrderDetail
from sqlalchemy import or_, and_, desc


def getPackages(id=None, packTypeCode=None, sexCode=None, maritalCode=None):
    session = getSession()
    try:
        qry = session.query(MiniProgPackages)
        if id is not None:
            return qry.get(id)
        else:
            if packTypeCode:
                qry = qry.filter(
                    or_(MiniProgPackages.packTypeCode == packTypeCode, MiniProgPackages.packTypeCode == None))
            if sexCode:
                qry = qry.filter(or_(MiniProgPackages.sexCode == sexCode, MiniProgPackages.sexCode == None))
            if maritalCode:
                qry = qry.filter(or_(MiniProgPackages.maritalCode == maritalCode, MiniProgPackages.maritalCode == None))
            return qry.all()
    finally:
        session.close()


def getPackageDetails(packageId):
    session = getSession()
    try:
        return session.query(MiniProgPackageDetails).filter(MiniProgPackageDetails.packageId == packageId).all()
    finally:
        session.close()


def getBasicInfo(certId):
    session = getSession()
    try:
        return session.query(MiniProgBaseInfo).filter(
            and_(or_(MiniProgBaseInfo.cert_id == certId.upper(), MiniProgBaseInfo.cert_id == certId.lower()),
                 MiniProgBaseInfo.symbol == '有效')).first()
    finally:
        session.close()


def getOrderDigest(personId):
    session = getSession()
    try:
        return session.query(MiniProgOrderDigest).filter(
            MiniProgOrderDigest.person_id == personId).filter(MiniProgOrderDigest.exam_status == '已预约').filter(
            MiniProgOrderDigest.symbol == '有效').order_by(
            desc(MiniProgOrderDigest.id)).first()

    finally:
        session.close()


def getOrderDigestByOrderId(orderId):
    session = getSession()
    try:
        return session.query(MiniProgOrderDigest).filter(
            MiniProgOrderDigest.id == orderId).filter(MiniProgOrderDigest.exam_status == '已预约').filter(
            MiniProgOrderDigest.symbol == '有效').all()
    finally:
        session.close()


def getOrders(certId):
    session = getSession()
    try:
        return session.query(MiniProgOrders).filter(
            or_(MiniProgOrders.certId == certId.upper(), MiniProgOrders.certId == certId.lower())).all()
    finally:
        session.close()


def getReportListByOrderDate(beginDate, endDate):
    session = getSession()
    try:
        query = session.query(MiniProgReportList)
        if beginDate:
            query = query.filter(MiniProgReportList.orderCheckDate >= beginDate)
        if endDate:
            query = query.filter(MiniProgReportList.orderCheckDate < endDate)
        return query.all()
    finally:
        session.close()


def getReportList(certId, beginDate, endDate):
    session = getSession()
    try:
        query = session.query(MiniProgReportList).filter(
            or_(MiniProgReportList.certId == certId.upper(), MiniProgReportList.certId == certId.lower()))
        if beginDate:
            query = query.filter(MiniProgReportList.examTime >= beginDate)
        if endDate:
            query = query.filter(MiniProgReportList.examTime <= endDate)
        return query.all()
    finally:
        session.close()


"""
  体检报告相关的操作
"""


def getReportBasicInfo(orderId):
    """
    根据预约号，获取人员基本信息
    :param orderId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgBasicInfo).filter(MiniProgBasicInfo.order_id == orderId).first()
    finally:
        session.close()


def getReportItemsResult(orderId):
    """
    根据预约号，获取项目结果信息
    :param orderId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgItemResults).filter(MiniProgItemResults.order_id == orderId).all()
    finally:
        session.close()


def getReportSummaries(orderId):
    """
    根据预约号，获取项目组小结
    :param orderId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgSummaries).filter(MiniProgSummaries.order_id == orderId).all()
    finally:
        session.close()


def getReportMainCheck(orderId):
    """
    根据预约号，获取主检信息
    :param orderId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgMainCheck).filter(MiniProgMainCheck.order_id == orderId).all()
    finally:
        session.close()


def getTeamOrderByCertId(certId):
    """
    根据身份证号，获取最近的一次状态为已预约的号码
    :param certId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgTeamOrder).filter(
            or_(MiniProgTeamOrder.cert_id == certId.upper(), MiniProgTeamOrder.cert_id == certId.lower())).order_by(
            desc(MiniProgTeamOrder.order_id)).first()

    finally:
        session.close()


def getTeamOrderDetail(orderId):
    """
    根据预约号，获取团检中的个检信息
    :param orderId:
    :return:
    """
    session = getSession()
    try:
        return session.query(MiniProgTeamOrderDetail).filter(MiniProgTeamOrderDetail.order_id == orderId).all()
    finally:
        session.close()
