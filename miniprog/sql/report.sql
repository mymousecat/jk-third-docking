
-- 报告视图 人员基本信息
drop view if EXISTS v_miniprog_report_basicinfo;
CREATE VIEW  v_miniprog_report_basicinfo AS
SELECT
  porder.ID AS ORDER_ID,
  person.EXAM_NO,
  person.CERT_ID,
  person.USERNAME,
  sexdict.BASE_VALUE AS GENDER,
  person.BIRTHDAY,
  nationdict.BASE_VALUE AS NATION,
  person.TELEPHONE,
  person.ADDRESS,
  person.EMAIL,
  person.IF_FAMILY,
  person.NATIVE_PLACE,
  person.INITIAL_TIME,
  person.CHANGE_TIME,
  org.ID AS ORG_ID,
  org.name AS ORG_NAME,
  contract.ID AS CONTRACT_ID,
  contract.`NAME` AS CONTRACT_NAME,
  customer.BASE_VALUE AS CUSTOMER_SOURCE,
  porder.DEPARTMENTS as DEPARTMENTS,
  porder.JOB_NUMBER,
  porder.POST,
  examtype.BASE_VALUE AS EXAM_TYPE,
  porder.EXAM_TIMES,
  porder.AGE,
  marital.BASE_VALUE AS MARITAL_STATUS,
  porder.ARRIVAL_DATE,
  porder.INITIAL_TIME AS ORDER_INITIAL_TIME,
  operator.REAL_NAME AS ORDER_STAFF
FROM
   t_personal_order porder
INNER JOIN t_person person ON porder.PERSON_ID = person.id
INNER JOIN t_base_dict sexdict ON person.SEX = sexdict.BASE_CODE AND sexdict.TYPE = '性别'
LEFT JOIN t_base_dict nationdict ON person.NATION = nationdict.BASE_CODE AND nationdict.TYPE = '民族'
LEFT JOIN t_organization org ON porder.ORGANIZATION_ID = org.ID
LEFT JOIN t_contract contract ON porder.contract_id = contract.ID
LEFT JOIN t_base_dict customer ON porder.CUSTOMER_SOURCE = customer.BASE_CODE AND customer.TYPE = '客户来源'
LEFT JOIN t_base_dict examtype ON porder.EXAM_TYPE = examtype.BASE_CODE AND examtype.TYPE = '体检类别'
LEFT JOIN t_base_dict marital ON porder.MARITAL_STATUS = marital.BASE_CODE AND marital.TYPE = '婚姻状态'
LEFT JOIN t_operator operator ON porder.initiator = operator.ID
WHERE
  porder.SYMBOL = '有效';

grant select on v_miniprog_report_basicinfo to 'third'@'%';



-- 报告视图 项目结果
drop view if EXISTS v_miniprog_report_items_result;
CREATE VIEW v_miniprog_report_items_result AS
SELECT
  results.id as ID,
  porder.id AS ORDER_ID,
  department.ID AS DEPARTMENT_ID,
  department.name AS DEPARTMENT_NAME,
  deptclass.BASE_VALUE AS DEPTCLASS,
  department.DISPLAY_ORDER AS DEPARTMENT_DISPLAY_ORDER,
  assem.id AS ASSEM_ID,
  assem.name AS ASSEM_NAME,
  passem.giveup_status AS ASSEM_GIVEUP,
  assem.DISPLAY_ORDER AS ASSEM_DISPLAY_ORDER,
  '' AS ASSEM_TYPE,
  element.id AS ELEMENT_ID,
  element.name AS ELEMENT_NAME,
  results.ID AS ELEMENT_DISPLAY_ORDER,
  results.RESULT_CONTENT,
  results.MEASUREMENT_UNIT AS MEASUREMENT_UNIT,
  results.FERENCE_LOWER_LIMIT,
  results.FERENCE_UPPER_LIMIT,
  results.RESULT_TYPE,
  results.POSITIVE_SYMBOL AS POSITIVE_SYMBOL,
  results.GIVEUP_SYMBOL  AS GIVEUP_SYMBOL
FROM
  t_personal_order porder

INNER JOIN t_person_element_assem  passem on porder.id = passem.ORDER_ID

INNER JOIN t_element_results results ON porder.id = results.ORDER_ID and results.ELEMENT_ASSEM_ID = passem.ELEMENT_ASSEM_ID

INNER JOIN t_department department ON results.DEPARTMENT_ID = department.id

LEFT JOIN t_base_dict deptclass ON department.DEPT_CLASS = deptclass.BASE_CODE AND deptclass.TYPE = '科室类别'

INNER JOIN t_element_assem_sub assem ON passem.ELEMENT_ASSEM_ID = assem.id

-- LEFT JOIN t_base_dictionary assemtype ON assem.ASSEM_TYPE = assemtype.BASE_CODE AND assemtype.TYPE = '项目组类别'
INNER JOIN t_element_sub element ON results.ELEMENT_ID = element.id
where passem.SYMBOL = '有效'

ORDER BY
  department.display_order,
  assem.display_order,
  results.id;


grant select on v_miniprog_report_items_result to 'third'@'%';


-- 报告信息 结论
drop view if EXISTS v_miniprog_report_summaries;
CREATE OR REPLACE VIEW v_miniprog_report_summaries AS

SELECT
  deta.id as ID,
  summary.ORDER_ID AS ORDER_ID,
  summary.DEPARTMENT_ID,
  summary.ELEMENT_ASSEM_ID AS ELEMENT_ASSEM_ID,
  operator.id AS OPERATOR_ID,
  operator.REAL_NAME AS OPERATOR_NAME,
  add_.ID AS ADDITIONAL_OPERATOR_ID,
  add_.REAL_NAME AS ADDITIONAL_OPERATOR_NAME,
  passem.COMPLETE_TIME,
  deta.DISEASE_CONTENT,
  deta.MERGE_WORD,
  deta.SELFWRITE_SYMBOL AS SELFWRITE_SYMBOL
FROM
  t_element_assem_summary summary
INNER JOIN t_element_assem_summary_deta deta ON summary.id = deta.ELEMENTCLASS_SUMMARY_ID
INNER JOIN t_person_element_assem passem on summary.ORDER_ID = passem.ORDER_ID and  summary.ELEMENT_ASSEM_ID = passem.ELEMENT_ASSEM_ID
LEFT JOIN t_operator operator ON summary.OPERATOR_ID = operator.id
LEFT JOIN t_operator add_ ON summary.ADDITIONAL_OPERATOR = add_.id
WHERE summary.CANCEL_SYMBOL = '有效' AND summary.SAVE_SYMBOL = '提交';


grant select on v_miniprog_report_summaries to 'third'@'%';


-- 报告信息 主检建议
drop view if EXISTS v_miniprog_report_maincheck;
CREATE OR REPLACE VIEW v_miniprog_report_maincheck AS
SELECT
  deta.ID as ID,
  porder.ID AS ORDER_ID,
  porder.EARLY_CHECK_UID,
  early.REAL_NAME AS EARLY_CHECK_NAME,
  porder.EARLY_CHECK_DATE,
  porder.MAIN_CHECK_UID,
  main.REAL_NAME AS MAIN_CHECK_NAME,
  porder.MAIN_CHECK_DATE,
  porder.FINAL_CHECK_UID,
  final.REAL_NAME AS FINAL_CHECK_NAME,
  porder.FINAL_CHECK_DATE,
  recheck.RECOMMEND,
  deta.DISEASE_ID,
  deta.MERGE_WORD
FROM
  t_personal_order porder
INNER JOIN t_recheck_result recheck ON porder.ID = recheck.ORDER_ID
INNER JOIN t_recheck_result_detail deta ON recheck.ID = deta.RECHECK_RESULT_ID
LEFT JOIN t_operator early ON porder.EARLY_CHECK_UID = early.ID
LEFT JOIN t_operator main ON porder.MAIN_CHECK_UID = main.ID
LEFT JOIN t_operator final ON porder.FINAL_CHECK_UID = final.ID;

grant select on v_miniprog_report_maincheck to 'third'@'%';
