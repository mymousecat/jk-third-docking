drop table if exists T_LIS_RESULT;

/*==============================================================*/
/* Table: T_LIS_RESULT                                          */
/*==============================================================*/
create table T_LIS_RESULT
(
   ID                   int not null auto_increment,
   BARCODE_ID           int,
   ORDER_ID             int,
   USERNAME             varchar(100),
   LIS_ELEMENT_ASSEM_ID varchar(100),
   LIS_ELEMENT_ASSEM_NAME varchar(100),
   LIS_ELEMENT_ID       varchar(100),
   LIS_ELEMENT_NAME     varchar(100),
   BLOOD_SAMPLE_SHAPE   varchar(100),
   CONTENT_RESULT       varchar(500),
   RESULT_UNIT          varchar(100),
   FERENCE_VALUE        varchar(500),
   FERENCE_LOWER_LIMIT  varchar(500),
   FERENCE_UPPER_LIMIT  varchar(500),
   POSITIVE_SYMBOL      varchar(100),
   CRITICAL_VALUES_SYMBO varchar(100),
   SAMPLE_DATE          datetime,
   SAMPLE_DOCTOR_ID     varchar(100),
   SAMPLE_DOCTOR        varchar(100),
   OPERATOR_ID          varchar(100),
   OPERATOR_NAME        varchar(100),
   AUDIT_ID             varchar(100),
   AUDIT_NAME           varchar(100),
   AUDIT_DATE           datetime,
   primary key (ID)
);

alter table T_LIS_RESULT comment '项目结果表';

/*==============================================================*/
/* Index: IDX_LIS_RESULT_BARCODE_ID                             */
/*==============================================================*/
create index IDX_LIS_RESULT_BARCODE_ID on T_LIS_RESULT
(
   BARCODE_ID
);

GRANT SELECT,INSERT,DELETE,UPDATE ON jk.T_LIS_RESULT TO 'third'@'%';