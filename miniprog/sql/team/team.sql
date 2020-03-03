
-- 根据身份证号，获取最新状态为已预约的预约号
drop view if EXISTS v_miniprog_team_cert_id;

create view v_miniprog_team_cert_id as
   select
     porder.id as order_id,
     basicinfo.cert_id
    from
    t_personal_order porder
    inner join t_person basicinfo on porder.PERSON_ID = basicinfo.id
    where   porder.SYMBOL = '有效' and porder.EXAM_STATUS = '已预约';


GRANT select on v_miniprog_team_cert_id to 'third'@'%';




-- 团检人员体检信息视图
drop view if EXISTS v_miniprog_team_order;

create view v_miniprog_team_order as
    select
      porder.id as order_id,
      porder.EXAM_STATUS,
      porder.reserve_check_date as order_exam_date,
      '01' as subarea_code,
      porder.age,
      '本体检中心' as subarea,
      basicinfo.exam_no as exam_no,
      basicinfo.cert_id,
      basicinfo.username,
      basicinfo.sex as sex_code,
      basicinfo.telephone,
      sexdict.base_value as sex,
      basicinfo.birthday,
      contract.id as company_id,
      contract.name as  company_name,
      contract.exam_begin_date,
      contract.exam_end_date,
      departments.id as department_id,
      departments.name as department_name,
      departments.display_order as department_display_order,
      itemcom.id as assem_id,
      itemcom.name as assem_name,
      itemcom.display_order as com_display_order,
      itemcom.CLINICAL_SYMBOLIFICANCE as clinical_significance,
      itemcom.DIRECT_PAGE_PROMPT as guidelines_single_prompt

    from
    t_personal_order porder
    inner join t_person as basicinfo on porder.PERSON_ID = basicinfo.id
    inner join t_organization company on porder.ORGANIZATION_ID = company.id
    inner join t_contract contract on porder.contract_id = contract.id
    inner join t_person_element_assem pcom on porder.id = pcom.ORDER_ID
    inner join t_element_assem_sub itemcom on pcom.ELEMENT_ASSEM_ID = itemcom.id
    inner join t_department departments on itemcom.DEPARTMENT_ID = departments.id
    inner join t_base_dict sexdict on basicinfo.sex = sexdict.base_code and sexdict.type = '性别'
    -- left  join t_base_dictionary subareadict on porder.reserve_subarea = subareadict.base_code and subareadict.type = '分区'
    where porder.SYMBOL = '有效' and porder.SYMBOL = '有效'
    order by departments.display_order,itemcom.display_order;

GRANT select on v_miniprog_team_order to 'third'@'%';
