-- 创建用户
create user lis identified by lis default tablespace PHEXAM_DATA_TBS;

grant connect,resource to lis;


create or replace view  V_LIS_BARCODE as
select barcode.id as barcode_id,
       basic.exam_no,
       porder.id as order_id,
       basic.username,
       basic.birthday,
       dict.base_value as sex_value,
       porder.age,
       basic.telephone,
       basic.address,
       spentype.base_value as   SPECIMEN_TYPE_NAME,
       combination.external_sys_control_code as LIS_ELEMENT_ASSEM_ID,
       combination.name as ELEMENT_ASSEM_NAME,
       null as LIS_ELEMENT_ID,
       null as ELEMENT_NAME,
       op.real_name as REQ_DOCTOR,
       porder.arrival_date as REQ_DATE
from
t_lab_barcode barcode
inner join t_lab_barcode_detail detail on barcode.id = detail.barcode_id
inner join t_personal_reservation porder on barcode.reserve_id = porder.id
inner join t_personal_base_info basic on porder.persion_id = basic.id
inner join t_item_combination_sub combination on detail.item_combination_id = combination.id
left join t_user op on porder.initiator = op.id
left join t_base_dictionary dict on basic.sex = dict.base_code and dict.type = '性别'
left join t_base_dictionary spentype on combination.specimen_type = spentype.base_code and spentype.type='标本类型';

grant select on V_LIS_BARCODE to lis;

create synonym lis.V_LIS_BARCODE for phexam.V_LIS_BARCODE;


create  sequence  s_lis_trans
 increment by 1
 start with 1
 nocache
 ;


create table t_lis_trans
(
   id                   int not null,
   barcode_id           varchar2(100),
   order_id             varchar2(100)  not null,
   element_assem_id     varchar2(100) not null,
   element_assem_name   varchar2(100) not null,
   username             varchar2(100),
   sex_name             varchar2(10),
   age                  varchar2(10),
   operator_id          varchar2(100),
   operator_name        varchar2(100),
   is_successfull       int,
   trans_msg            varchar2(4000),
   sample_date          date,
   trans_date           date default sysdate,
   trans_time           date default sysdate,
   primary key (id)
);



create index idx_lis_trans_order_id on t_lis_trans
(
   order_id
);


create or replace trigger tr_lis_trans
before insert on t_lis_trans for each row
begin
  select  s_lis_trans.nextval into :new.id from dual;
end;




