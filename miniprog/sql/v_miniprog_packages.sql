DROP VIEW
IF EXISTS v_miniprog_packages;

CREATE VIEW v_miniprog_packages AS SELECT
	pack.id,
	pack. NAME,
	pack.type AS "packTypeCode",
	packtype.base_value AS "packTypeName",
	pack.sex AS "sexCode",
	pack.display_order AS "displayOrder",
	sexdict.base_value AS "sexName",
	pack.marital_status AS "maritalCode",
	marital.base_value AS "maritalName",
	pack.original_price AS "originalPrice",
	pack.discount_price AS "discountPrice",
	pack.discount_rate AS "dicountRate",
	pack.CLINICAL_SYMBOLIFICANCE AS "clinicalSignificance",
	pack.initial_time AS "createTime",
	pack.change_time AS "changeTime"
FROM
	t_assem_package pack
LEFT JOIN t_base_dict packtype ON packtype.type = '套餐类别'
AND pack.type = packtype.base_code
LEFT JOIN t_base_dict sexdict ON sexdict.type = '性别'
AND pack.sex = sexdict.base_code
LEFT JOIN t_base_dict marital ON marital.type = '婚姻状态'
AND pack.marital_status = marital.base_code
WHERE
	pack.SYMBOL = '启用'
AND pack.type <> '3'
ORDER BY
	pack.display_order;

GRANT select on v_miniprog_packages to 'third'@'%';
