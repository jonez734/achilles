\echo symptom
create or replace view achilles.symptom as
  select n.*,
    (n.attributes->>'memberid')::bigint as memberid,
    (n.attributes->>'fooditemid')::bigint as fooditemid,
    (n.attributes->>'description')::text as description,
    (n.attributes->>'severity')::bigint as severity,
    (n.attributes->>'duration')::interval as duration,
    (n.attributes->>'remedy')::text as remedy
  from engine.node as n
  where n.prg='achilles.symptom'
;

grant select on achilles.symptom to "apache";

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
