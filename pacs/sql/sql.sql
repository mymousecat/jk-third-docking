-- 体检结果中间表

drop table if EXISTS  T_PACS_RESULT;
create table T_PACS_RESULT
(
   ID                   INT not null auto_increment,
   ORDER_ID             INT not null,
   PACS_ASSEM_ID        VARCHAR(50) not null,
   PACS_ASSEM_NAME      VARCHAR(100) not null,
   USERNAME             VARCHAR(50) not null,
   REPORT_DIAGNOSE      VARCHAR(2000) not null,
   REPORT_RESULT        VARCHAR(2000) not null,
   POSITIVE_CONTENT     VARCHAR(1000),
   REPORT_URL           VARCHAR(200),
   REPORTER_ID          VARCHAR(50),
   REPORTER             VARCHAR(50) not null,
   REPORT_DATE          DATETIME not null,
   AUDIT_DOCTOR_ID      VARCHAR(50),
   AUDIT_DOCTOR         VARCHAR(50) not null,
   AUDIT_DATE           DATETIME not null,
   primary key (ID)
);

create index IDX_PACS_RESULT_ORDER_ID on T_PACS_RESULT
(
  ORDER_ID
);


GRANT SELECT,INSERT,DELETE
	on T_PACS_RESULT to 'third'@'%';


-- 项目组登记表
drop table if EXISTS T_PACS_REG;
create table T_PACS_REG
(
   ID                   int not null auto_increment,
   ORDER_ID             int not null,
   PACS_ASSEM_ID        varchar(50) not null,
   PACS_ASSEM_NAME      varchar(100) not null,
   MODALITY             varchar(10) not null,
   OP_TYPE              varchar(20) not null,
   OP_NAME              varchar(50) not null,
   primary key (ID)
);

GRANT SELECT,INSERT,DELETE
	on T_PACS_REG to 'third'@'%';


-- 日志传输表
drop table if EXISTS T_PACS_TRANS_LOG;
create table T_PACS_TRANS_LOG
(
   ID int not null auto_increment,
   ORDER_ID             int not null,
   PACS_ASSEM_ID        varchar(50) not null,
   PACS_ASSEM_NAME      varchar(100) not null,
   LOG_TYPE             varchar(20),
   MSG                  varchar(4000),
   TRANS_TIME           datetime,
    primary key (ID)
);

create index IDX_PACS_TRANS_LOG_ORDER_ID on T_PACS_TRANS_LOG
(
  ORDER_ID
);

GRANT SELECT,INSERT,DELETE,UPDATE
	on T_PACS_TRANS_LOG to 'third'@'%';



DROP VIEW
IF EXISTS V_PACS;

CREATE VIEW V_PACS AS SELECT
	a.EXAM_NO,
	b.ID AS ORDER_ID,
	a.USERNAME AS USERNAME,
	(
		CASE
		WHEN (a.SEX = '1') THEN
			'男'
		ELSE
			'女'
		END
	) AS SEX_NAME,
	DATE_FORMAT(a.BIRTHDAY, '%Y-%m-%d') AS BIRTHDAY,
	b.AGE,
	a.CERT_ID,
	a.TELEPHONE,
	a.ADDRESS,
	CASE
WHEN d.DEPARTMENT_ID = 6 THEN
	'DR'
WHEN d.DEPARTMENT_ID = 20 THEN
	'CT'
WHEN d.DEPARTMENT_ID = 21 THEN
	'MR'
WHEN d.DEPARTMENT_ID = 35 THEN
	'ESP'
WHEN d.DEPARTMENT_ID = 5 THEN
	'US'
END AS MODALITY,
 c.DISCOUNT_PRICE AS FEE,
 d.ID AS PACS_ASSEM_ID,
 d. NAME AS ASSEM_NAME,
 -- element.ID AS PACS_ELEMENT_ID,
 -- element. NAME AS ELEMENT_NAME,
 z.REAL_NAME AS REQ_DOCTOR,
 now() AS REQ_DATE
FROM
	t_person a
JOIN t_personal_order b ON a.ID = b.PERSON_ID
JOIN t_person_element_assem c ON c.ORDER_ID = b.ID
JOIN t_element_assem_sub d ON c.ELEMENT_ASSEM_ID = d.ID
-- JOIN t_element_assem_detail_sub detail ON detail.ELEMENT_ASSEM_ID = d.id
-- JOIN t_element_sub element ON detail.ELEMENT_ID = element.ID
JOIN t_operator z ON z.ID = c.INITIATOR
WHERE
	b.EXAM_STATUS <> '已预约'
AND c.UNIT_OR_OWN = '公费'
OR (
	c.UNIT_OR_OWN = '自费'
	AND c.COST_STATUS = '已收'
)
AND ISNULL(c.LOGIN_TIME)
AND c.COMPLETE_STATUS = '未完成';

GRANT SELECT
	ON jk.v_pacs TO 'third'@'%';

GRANT SELECT
	ON t_element_assem_sub TO 'third'@'%';



DROP VIEW
IF EXISTS V_ASSEM_BARCODE;

CREATE VIEW V_ASSEM_BARCODE AS SELECT
	barcode.ID AS CHECK_NO,
	porder.ID AS ORDER_ID,
	person.USERNAME,
	person.CERT_ID,
	person.BIRTHDAY,
	dict.BASE_VALUE AS SEX_NAME,
	porder.AGE,
	person.TELEPHONE,
	person.ADDRESS,
	CASE
WHEN sub.DEPARTMENT_ID = 6 THEN
	'DR'
WHEN sub.DEPARTMENT_ID = 20 THEN
	'CT'
WHEN sub.DEPARTMENT_ID = 21 THEN
	'MR'
WHEN sub.DEPARTMENT_ID = 35 THEN
	'ESP'
END AS MODALITY,
 sub.ID AS PACS_ASSEM_ID,
 sub. NAME AS ASSEM_NAME,
 op.REAL_NAME AS REQ_DOCTOR,
 porder.ARRIVAL_DATE AS REQ_DATE
FROM
	t_personal_order porder
INNER JOIN t_person person ON porder.PERSON_ID = person.ID
LEFT JOIN t_base_dict dict ON person.SEX = dict.BASE_CODE
AND dict.TYPE = '性别'
INNER JOIN t_barcode barcode ON porder.ID = barcode.ORDER_ID
INNER JOIN t_barcode_detail detail ON detail.BARCODE_ID = barcode.ID
inner join t_person_element_assem passem on porder.ID = passem.ORDER_ID and passem.ELEMENT_ASSEM_ID = detail.ELEMENT_ASSEM_ID

INNER JOIN t_element_assem_sub sub ON detail.ELEMENT_ASSEM_ID = sub.ID
LEFT JOIN t_operator op ON porder.INITIATOR = op.ID
WHERE
	sub.DEPARTMENT_ID IN (6, 20, 21, 35)
  and passem.SYMBOL = '有效'
  and porder.EXAM_STATUS <> '已预约'
  and
  (
     (passem.UNIT_OR_OWN = '公费')
     or
      (
        passem.UNIT_OR_OWN = '自费' and passem.COST_STATUS = '已收'
     )
  );

GRANT SELECT
	ON V_ASSEM_BARCODE TO 'third'@'%';

