-- 申请项目（化验类，如：医嘱项目） v_lis_clinicitem
DROP VIEW
IF EXISTS v_lis_clinicitem;

CREATE VIEW v_lis_clinicitem AS SELECT
	assem.ID AS item_code,
	assem.`NAME` AS item_name,
	assem.PRICE AS Price,
	'验检' AS Item_class,
	'验检科' AS Exec_dept

FROM
	t_element_assem_sub AS assem
  where assem.DEPARTMENT_ID in (3,34);

-- select * from t_element_assem_sub;
GRANT SELECT
	ON v_lis_clinicitem TO 'third'@'%';

