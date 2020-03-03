-- 获取申请单信息视图 get_req_info (一般发生在由HIS/体检系统开单并打印条码，LIS系统在签收标本时调用获取信息)
DROP VIEW
IF EXISTS get_req_info;

CREATE VIEW get_req_info AS SELECT
	'C' AS reqtype,
	-- 申请类别  C=检验，H＝输血，为空也视作检验
	barcode.ID AS barcode,
	-- 申请单号/条码号 返回AUTOADD则表示由LIS系统自动分配条码号，每次都会分配REQ+reqid格式的条码
	'' AS hospitalcode,
	-- 送检医院代码，本院送检的不填
	'4' AS pat_type, -- 病人类型  1＝门诊，2＝急诊，3＝住院，4＝体检等，体检时也可直接保存名称
  barcode.ORDER_ID as pat_no, -- 病人号  就诊号门诊为门诊号住院为住院号（习惯号码）
  person.EXAM_NO as pat_id,  -- 病人唯一号  内部的唯一号，接病人id比较时使用
  '' as pat_cardno,   -- 就诊卡号
  barcode.ORDER_ID as inp_id,  -- 住院标识  用于区分同一住院号多次住院，门诊用于保存就诊序号
  porder.ARRIVAL_DATE as inp_date, -- 住院为入院日期，门诊为就诊日期
  person.USERNAME as pat_name,  -- 病人姓名
  sexdict.BASE_VALUE as pat_sex, -- 性别  1男，2女，3未知（系统支持识别：男、女、M、F）
  person.BIRTHDAY as pat_birth, -- 病人生日日期 如：1975-05-11 或年龄字串  如：1岁，12月23天，这样的格式都支持
  '' as pat_diag, -- 临床诊断
  '自费' as charge_typeno, -- 收费类型 如：自费、医保等
  '' as  req_wardno, -- 病人病区代码
  '' as req_bedno, -- 病人床号
  '' as req_comm, -- 医生备注  开单时由医生填写的备注信息
  '3' as req_deptno, -- 申请科室代码
  operator.REAL_NAME as req_docno,   -- 申请医生
  porder.ARRIVAL_DATE as  req_dt, -- 申请时间
  '0' as emer_flag,  -- 加急标志  急诊状态0非急1急
  '' as original_reqno, -- 原始单号  HIS系统中的申请单号，外来标本的原始申请号条码号，如无为空
  '' as perform_dept, -- 执行科室
  assem.CLINICAL_SYMBOLIFICANCE as req_groupna,  -- 申请单类别 如：生化、免疫、临检等
  specimendict.BASE_VALUE as  specimen_name,  -- 标本类型 如：血、尿等
  '' as sample_detail, -- 标本备注说明
  '' as req_reason,    -- 送检目的
  '' as sample_items,  -- 项目描述  默认保存打印在条码标签上的检验项目内容，多个一般用逗号隔开，
  '' as print_dt, -- 打印时间
  '' as print_user, -- 打印者
  0 as print_count, -- 打印次数
  passem.BLOOD_TIME as sampled_dt, -- 采样时间
  bloodoper.REAL_NAME as sampled_user, -- 采样者
  '' as send_dt, -- 护士移交给护工的时间
  '' as send_user, -- 交接护工
  '' as cancel_dt, -- 作废时间
  '' as cancel_user, -- 作废用户
  '1' as charge_flag, -- 收费标志  0未收费1已收费9已退费
  '' as  charge_user, -- 计价人
  '' as charge_dt,  -- 计价时间
  assem.PRICE as base_amount, -- 申请单应收总金额
  passem.DISCOUNT_AMOUNT as amount, -- 申请单实收总金额
  '' as secrecy, -- 加密标志
  '' as other_stat, -- 备用标志  备用状态，可能his中以后会遇到在状态
  '' as abo_bldtype, -- ABO血型  A/B/AB/O
  '' as rh_bldtype, -- RH血型  +,- 表示阴性、阳性
  '' as bld_usedt,  -- 计划用血时间
  '' as bld_reason, -- 输血目的 （手术、治疗、抢救、备血）
  'N' as bld_transfused, -- 既往有输血史  1＝有，0＝无，N＝不详
  'N' as bld_pregnancyed, -- 既往有妊娠史  1＝有，0＝无，N＝不详
  -1 as bld_pregcount, -- 孕育次数  -1为不详
  -1 as  bld_birthcount, -- 生产次数  -1为不详
  'N' as bld_reaction, -- 输血不良反应记录  1＝有，0＝无，N＝不详
  '' as saleman, -- 所属销售人  用于独立检验中心的销售员记录，便于统计核算
  '' as pat_diag_icd, -- 诊断的ICD10编码
  person.ADDRESS as pat_address, -- 病人联系地址
  '中国' as pat_nation, -- 国籍
  person.CERT_ID as  pat_idcardno,  -- 身份证号护照号
  person.TELEPHONE as pat_phone, -- 联系电话
  0 as pat_height, --  身高  单位cm，如：175
  0 as weight, -- 体重  单位kg，如：58.5
  '0' as  ReqSource, -- 申请单来源 0=外部系统申请单,1=LIS门诊采血生成,3=病区护士站生成,21=输入病历号开窗选取项目后生成,22=Lis系统登记生成,其他以后拓展
  -- 标本接收时间（针对由其他LIS签收，然后在lis6中检验的情况，多用于切换lis）
  -- 标本接收人（针对由其他LIS签收，然后在lis6中检验的情况，多用于切换lis）
  '' as  send_user1, -- 运送人（针对移动标本交接时记录的运送人并且检验科派人到临床交接标本的情况）
  barcode.ID as  his_recordid, -- 申请明细记录号 通过本字段可以追踪到HIS中一条医嘱或者一条申请项目记录，可以使用多个字段联合成唯一号
  bdetail.ID as  seq,  -- 序号
  assem.EXTERNAL_SYS_CONTROL_CODE as  req_itemcode, -- 申请项目代码
  assem.`NAME` as req_itemname, -- 申请项目名称
  assem.`NAME` as combitemna, --  所属组合名称（如H开组套肝功能，包含10个小项，则返回10条记录，本字段都是“肝功能）
  assem.PRICE as base_price, -- 项目基准价格  检验中心时填入区域价格，普通医院填入项目单价
  passem.DISCOUNT_PRICE as item_price,  -- 项目实际价格  检验中心时填入实际价格，普通医院开单时填入项目单价
  assem.ID as his_itemcode, -- HIS中原始申请项目代码
  1 as qty,   -- 数量  检验一般都是1，用血时为具体申请数量
  -- passem.DISCOUNT_PRICE as amount -- 项目金额
  '' as his_refcol1, -- HIS表相关备用字段1  备用，由于RecordID有时候是几个字段组合成的，编程序回调时可能需要拆分，导致编码（或者存储过程）编写不便，所以可以使用这三个字段冗余相关HIS信息
  '' as his_refcol2, --  HIS表相关字段2
  '' as his_refcol3, -- HIS表相关字段3
  '1' as BLD_SelfFlag,-- 自身输血标志 1表示自身输血
  '01' as  BLD_Selftype, -- 自身输血类别 01=储存式 02=稀释式 03=回收式，其他以后扩展，来源系统代码表Kind=BLD_Selftype
  '01' as  bldSelf_CollectType  -- 自身输血采血方式 01=单纯式 02=蛙跳式 ，其他以后扩展，来源系统代码表Kind=BLDSELF_COLLECTTYPE

FROM
	t_barcode barcode

  left join t_barcode_assem_class barcodeclass on barcode.BARCODE_ASSEM_TYPE_ID = barcodeclass.ID
  left join t_base_dict as specimendict on barcodeclass.SPECIMEN_TYPE = specimendict.BASE_CODE and specimendict.TYPE = '标本类型'

  inner join t_barcode_detail bdetail on bdetail.BARCODE_ID = barcode.ID
  inner join t_personal_order porder on barcode.ORDER_ID = porder.ID
  inner join t_person person on porder.PERSON_ID = person.ID
  left join t_base_dict sexdict on person.SEX = sexdict.BASE_CODE and sexdict.TYPE = '性别'
  left join t_operator operator on porder.INITIATOR = operator.ID
  inner join t_person_element_assem passem on passem.ORDER_ID = porder.ID and passem.ELEMENT_ASSEM_ID = bdetail.ELEMENT_ASSEM_ID and passem.SYMBOL = '有效'
  inner join t_element_assem_sub assem on passem.ELEMENT_ASSEM_ID = assem.ID
  left join t_operator bloodoper on passem.BLOOD_OPERATOR = bloodoper.ID;

grant select on get_req_info to 'third'@'%';