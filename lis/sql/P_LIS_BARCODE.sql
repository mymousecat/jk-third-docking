DROP VIEW
IF EXISTS V_LIS_BARCODE;

CREATE VIEW V_LIS_BARCODE AS SELECT
	concat(a.id, e.id) AS ID,
	a.ID AS BARCODE_ID,
	b.EXAM_NO AS EXAM_NO,
	c.ID AS ORDER_ID,
	b.USERNAME AS USERNAME,
	date_format(b.BIRTHDAY, '%Y-%m-%d') AS BIRTHDAY,
	sex.BASE_VALUE AS SEX_NAME,
	c.AGE AS AGE,
	b.TELEPHONE AS TELEPHONE,
	b.ADDRESS AS ADDRESS,
	specimen.BASE_VALUE AS SPECIMEN_TYPE_NAME,
	e.EXTERNAL_SYS_CONTROL_CODE AS LIS_ELEMENT_ASSEM_ID,
	e. NAME AS ELEMENT_ASSEM_NAME,
	e.ID AS ELEMENT_ID,
	e. NAME AS ELEMENT_NAME,
	oper.REAL_NAME AS REQ_DOCTOR,
	c.ARRIVAL_DATE AS REQ_DATE,
	e.DISPLAY_ORDER AS DISPLAY_ORDER
FROM
	t_barcode a
JOIN t_personal_order c ON a.ORDER_ID = c.ID
JOIN t_person b ON c.PERSON_ID = b.ID
JOIN t_base_dict sex ON b.SEX = sex.BASE_CODE
AND sex.TYPE = '性别'
JOIN t_barcode_detail g ON g.BARCODE_ID = a.ID
JOIN t_element_assem_sub e ON g.ELEMENT_ASSEM_ID = e.ID
JOIN t_barcode_assem_class barcodeclass ON a.BARCODE_ASSEM_TYPE_ID = barcodeclass.ID
LEFT JOIN t_base_dict specimen ON barcodeclass.SPECIMEN_TYPE = specimen.BASE_CODE
AND specimen.TYPE = '标本类型'
LEFT JOIN t_operator oper ON c.INITIATOR = oper.ID
WHERE
	c.EXAM_STATUS <> '已预约'
AND c.SYMBOL = '有效';

GRANT SELECT
	,
	SHOW VIEW ON jk.v_lis_barcode TO 'third'@'%';