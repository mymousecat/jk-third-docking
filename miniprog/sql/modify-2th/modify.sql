
-- 在返回的套餐明细中，增加小项
drop view if EXISTS v_miniprog_package_detail;

create  view v_miniprog_package_detail as
select
   CONCAT(detail.ELEMENT_ASSEM_ID , '-' , item.id) as id,
   detail.ELEMENT_ASSEM_ID as "groupId",
   com.name as "groupName",
   detail.original_price as "originalPrice",
   detail.discount_price as "discountPrice",
   detail.discount_rate as "dicountRate",
   detail.display_order as "displayOrder",
   com.CLINICAL_SYMBOLIFICANCE as "clinicalSignificance",
   com.DIRECT_PAGE_PROMPT as attention,
   com.DEPARTMENT_ID as "departmentId",
   department.name as "departmentName",
   detail.package_id as "packageId",
   item.id as "itemId",
   item.name as "itemName"
from

t_assem_package_detail detail
inner join t_element_assem_sub com on detail.ELEMENT_ASSEM_ID = com.id
inner join t_department department on com.DEPARTMENT_ID = department.id
inner join t_element_assem_detail_sub detail_sub on detail_sub.ELEMENT_ASSEM_ID = com.id
inner join t_element_sub  item on item.id = detail_sub.ELEMENT_ID
order by detail.display_order;


grant select on v_miniprog_package_detail to 'third'@'%';


-- 返回生成报告的列表
drop  view if EXISTS v_miniprog_get_report_list;

create view  v_miniprog_get_report_list as
select
  baseinfo.exam_no as "examNo",
  baseinfo.cert_id as "certId",
  baseinfo.username,
  baseinfo.birthday as birth,
  baseinfo.sex as "sexCode",
  case baseinfo.sex
    when '1' then '男'
    when '2' then '女'
  end sex,
  res.id as "orderId",
  res.age,
  company.id as "companyId",
  company.`NAME` as "companyName",
  res.arrival_date as "examTime",
  res.exam_type as "examTypeCode",
  base_examtype.base_value as "examType",
  res.main_check_uid as "mainCheckUid",
  maincheckop.real_name as "mainCheckDoctor",
  res.main_check_date as "mainCheckTime",
  res.final_check_uid as "finalCheckUid",
  finalcheckop.real_name as "finalCheckDoctor",
  res.main_check_date as "finalCheckTime"
from
t_personal_order res
inner join t_person baseinfo on res.PERSON_ID = baseinfo.id
left join t_organization company on res.ORGANIZATION_ID = company.id
inner join t_base_dict base_examtype on res.exam_type = base_examtype.base_code and base_examtype.type = '体检类别'
left join t_operator maincheckop on res.MAIN_CHECK_UID =  maincheckop.id
left join t_operator finalcheckop on res.FINAL_CHECK_UID = finalcheckop.id
where res.SYMBOL = '有效' and  res.exam_status  in  ('报告已交接','终检完成','报告送达','报告已打印');
-- 体检类型 并且 单位类型 都不是军免，才可以查询的到
-- and  (res.exam_type <> '02' and  company.company_type <> '军免');


grant select on v_miniprog_get_report_list to 'third'@'%';
