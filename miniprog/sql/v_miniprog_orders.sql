
drop view if EXISTS v_miniprog_orders;

create view v_miniprog_orders as
select
      CONCAT(res.id , '_' , pcom.ELEMENT_ASSEM_ID) as id,
      basic.exam_no as "examNo",
      basic.cert_id as "certId",
      basic.username,
      basic.sex as "sexCode",
      sexDict.Base_Value as sex,
      basic.birthday as birth,
      res.age,
      basic.telephone as mobile,
      res.id as "orderId",
      res.customer_source as "customerSourceCode",
      sour.base_value as "customerSource",
      res.exam_type as "examTypeCode",
      examT.Base_Value as "examType",
      res.marital_status as "maritalCode",
      marial.base_value as marital,
      res.exam_status as "examStatus",
      res.initial_time as "orderTime",
      res.arrival_date as "examTime",
      res.reserve_check_date as "orderExamTime",
      '01' as "subareaCode",
      '本体检中心' as subarea,
      null as "packageId",
      null as "packageName",
      depart.id as "departmentId",
      depart.name as "departmentName",
      depart.display_order as "departmentDisplayOrder",
      pcom.ELEMENT_ASSEM_ID as "groupId",
      sub.name as "groupName",
      sub.display_order as "groupDisplayOrder",
      sub.CLINICAL_SYMBOLIFICANCE as "clinicalSignificance",
      pcom.original_price as "originalPrice",
      pcom.discount_price as "discountPrice",
      pcom.discount_rate as "discountRate",
      pcom.Unit_Or_Own as "feeType",
      pcom.cost_status as "costStatus",


pcom.Complete_Status AS "completeStatus",

      pcom.login_time as "completeTime"
from t_personal_order res
inner join t_person basic on res.PERSON_ID = basic.id
left join t_base_dict sexDict on basic.sex = sexDict.Base_Code and sexDict.Type = '性别'
left join t_base_dict sour on res.customer_source = sour.base_code and sour.type = '客户来源'
left join t_base_dict examT on res.exam_type = examT.Base_Code and examT.Type = '体检类别'
left join t_base_dict marial on res.marital_status = marial.base_code and marial.type = '婚姻状态'
-- left join t_assem_package pack on to_number(res.reserved3) = pack.id
inner join t_person_element_assem pcom on res.id = pcom.ORDER_ID
inner join t_element_assem_sub sub on pcom.ELEMENT_ASSEM_ID = sub.id
inner join t_department depart on sub.department_id = depart.id

where res.SYMBOL = '有效'  and pcom.SYMBOL = '有效'

order by depart.display_order,sub.display_order ;

GRANT select on v_miniprog_orders to 'third'@'%';