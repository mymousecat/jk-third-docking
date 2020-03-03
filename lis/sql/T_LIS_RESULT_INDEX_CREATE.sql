alter table t_lis_result  add constraint pk_result_id primary key(ID); 
create index idx_result_barcode_id on t_lis_result(BARCODE_ID);
