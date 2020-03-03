
drop view  if EXISTS v_miniprog_package_detail;

CREATE VIEW v_miniprog_package_detail AS

select
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
   detail.PACKAGE_ID as "packageId"
from
t_assem_package_detail detail
inner join t_element_assem_sub com on detail.ELEMENT_ASSEM_ID = com.ID
inner join t_department department on com.DEPARTMENT_ID = department.ID
order by detail.DISPLAY_ORDER;

GRANT select on v_miniprog_package_detail to 'third'@'%';
