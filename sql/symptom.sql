create table achilles.__symptom (
  "id" serial unique not null primary key,
  "description" text not null,
  "severity" text not null,
  "duration" interval,
  "remedy" text,
  "dateposted" timestamptz,
  "postedbyid" integer constraint fk_symptom_postedbyid references engine.__member(id) on update cascade on delete set null,
  "datemodified" timestamptz,
  "modifiedbyid" integer constraint fk_symptom_modifiedbyid references engine.__member(id) on update cascade on delete set null
);

grant all on achilles.__symptom to "apache";

create view achilles.symptom as 
  select 
    achilles.__symptom.*, 
    extract(epoch from achilles.__symptom.datemodified) as datemodifiedepoch,
    extract(epoch from achilles.__symptom.dateposted) as datepostedepoch
  from achilles.__symptom
;
