\echo symptom
create or replace view achilles.symptom as
  select b.*,
    (b.attributes->>'memberid')::bigint as memberid,
    (b.attributes->>'fooditemid')::bigint as fooditemid,
    (b.attributes->>'description')::text as description,
    (b.attributes->>'severity')::bigint as severity,
    (b.attributes->>'duration')::interval as duration,
    (b.attributes->>'remedy')::text as remedy
  from engine.__blurb as b
  where b.prg='achilles.symptom'
;

grant select on achilles.symptom to :web;

--create table achilles.__symptom (
--  "id" serial unique not null primary key,
--  "description" text not null,
--  "severity" text not null,
--  "duration" interval,
--  "remedy" text,
--  "dateposted" timestamptz,
--  "postedbyid" integer constraint fk_symptom_postedbyid references engine.__member(id) on update cascade on delete set null,
--  "datemodified" timestamptz,
--  "modifiedbyid" integer constraint fk_symptom_modifiedbyid references engine.__member(id) on update cascade on delete set null
--);

--grant all on achilles.__symptom to "apache";

--create view achilles.symptom as 
--  select 
--    achilles.__symptom.*, 
--    extract(epoch from achilles.__symptom.datemodified) as datemodifiedepoch,
--    extract(epoch from achilles.__symptom.dateposted) as datepostedepoch
--  from achilles.__symptom
--;
