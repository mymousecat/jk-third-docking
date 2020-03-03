create index idx_personcertid on t_person
(
  cert_id
);


create index idx_base_dict_c on t_base_dict
(
  type,
  base_code
);
