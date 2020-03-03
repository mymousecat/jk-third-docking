
-- 基本信息
DROP VIEW
IF EXISTS v_yibao_basicinfo;

CREATE VIEW v_yibao_basicinfo AS SELECT
	porder.ID AS order_id,
	person.SEX,
	person.USERNAME,
	person.CERT_ID,
	porder.AGE,
	person.TELEPHONE,
	porder.JOB_NUMBER,
	porder.ARRIVAL_DATE,
  op.REAL_NAME as MAIN_CHECK_DOCTOR
FROM
	t_personal_order porder
INNER JOIN t_person person ON porder.PERSON_ID = person.ID
left JOIN t_operator op on porder.MAIN_CHECK_UID = op.ID;


GRANT SELECT
	ON v_yibao_basicinfo TO 'third'@'%';



-- 项目结果表
DROP VIEW
IF EXISTS v_yibao_itemresult;

CREATE VIEW v_yibao_itemresult AS SELECT
	result.ID,
	result.ORDER_ID,
	department.ID AS department_id,
	department.`NAME` AS department_name,
	assem.id AS assem_id,
	assem.`NAME` AS assem_name,
	addop.REAL_NAME AS addop_name,
	op.REAL_NAME AS doc_name,
	element.ID AS element_id,
	element. NAME AS element_name,
	element.MAP_CODE,
	result.RESULT_TYPE,
	result.RESULT_CONTENT,
	result.MEASUREMENT_UNIT AS unit,
	result.FERENCE_LOWER_LIMIT AS low,
	result.FERENCE_UPPER_LIMIT AS upper,
	result.POSITIVE_SYMBOL AS positive,
  result.GIVEUP_SYMBOL,
	element.DEFAULT_VALUE
FROM
	t_element_results result
INNER JOIN t_department department ON result.DEPARTMENT_ID = department.ID
INNER JOIN t_element_assem_sub assem ON result.ELEMENT_ASSEM_ID = assem.ID
LEFT JOIN t_operator addop ON result.ADDITIONAL_OPERATOR = addop.ID
LEFT JOIN t_operator op ON result.OPERATOR_ID = op.ID
INNER JOIN t_element_sub element ON result.ELEMENT_ID = element.ID
ORDER BY
	department.DISPLAY_ORDER,
	assem.DISPLAY_ORDER,
	result.ID;

GRANT SELECT
	ON v_yibao_itemresult TO 'third'@'%';


-- 项目组结论表
DROP VIEW
IF EXISTS v_yibao_summary;

CREATE VIEW v_yibao_summary AS SELECT
	deta.ID,
  summary.ORDER_ID,
	summary.ELEMENT_ASSEM_ID,
	deta.MERGE_WORD,
	deta.SELFWRITE_SYMBOL,
  disease.MAP_CODE

FROM
	t_element_assem_summary summary
INNER JOIN t_element_assem_summary_deta deta ON summary.ID = deta.ELEMENTCLASS_SUMMARY_ID
LEFT JOIN t_disease disease on disease.ID = convert(deta.DISEASE_CONTENT,SIGNED) and deta.SELFWRITE_SYMBOL = '01'
WHERE
	summary.SAVE_SYMBOL = '提交' AND summary.CANCEL_SYMBOL = '有效';

grant select on v_yibao_summary to 'third'@'%';


-- 主检建议表
DROP VIEW
IF EXISTS v_yibao_recheck;

CREATE VIEW v_yibao_recheck AS SELECT
  detail.ID,
	recheck.RECOMMEND,
	recheck.ORDER_ID,
	detail.MERGE_WORD
FROM
	t_recheck_result recheck
INNER JOIN t_recheck_result_detail detail ON recheck.ID = detail.RECHECK_RESULT_ID;

grant select on v_yibao_recheck to 'third'@'%';

grant select on t_exam_media to 'third'@'%';


create table t_yibao_trans_log
(
   id                   int not null auto_increment comment 'ID，自增',
   order_id             integer not null comment '预约号',
   trans_time           datetime COMMENT '转输时间',
   success              varchar(10) COMMENT '成功，还是失败',
   msg                  varchar(2000) COMMENT '失败的原因',
   CREATED              datetime not null default CURRENT_TIMESTAMP comment '生成记录的时间，默认为当前时间',
   primary key (ID)
);

create index idx_yibao_trans_log_order_id on t_yibao_trans_log
(
  order_id
);

GRANT select,insert,update,delete on t_yibao_trans_log to 'third'@'%';


FLUSH PRIVILEGES;

-- 体检报告完成触发器
DROP TRIGGER
IF EXISTS tr_yibao_up;

CREATE TRIGGER tr_yibao_up AFTER UPDATE ON t_personal_order FOR EACH ROW
BEGIN
	IF old.exam_status = '主检完成' AND new.exam_status = '终检完成' AND new.exam_type = '13' THEN
		INSERT INTO t_yibao_trans_log (order_id)
		VALUES
			(new.id);
	END IF;

END;
