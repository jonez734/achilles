create or replace view achilles.merchant as
    select n.*,
        (attributes->>'type') as type,
        (attributes->>'name') as name,
        (attributes->>'title') as title,
        (attributes->>'address') as address,
        (attributes->>'coordinates') as coordinates,
        (attributes->>'url') as url
    from engine.node as n
    where n.prg = 'achilles.merchant'
;

--create table achilles.__merchant (
--    "id" serial unique not null primary key,
--    "name" text unique,
--    "type" text,
--    "qsr" boolean default 'f',
--    "datecreated" timestamptz,
--    "createdbyid" integer  constraint fk_seller_createdbyid references engine.__member(id) on update cascade on delete set null,
--    "datemodified" timestamptz,
--    "modifiedbyid" integer constraint fk_fooditem_modifiedbyid references engine.__member(id) on update cascade on delete set null
--);
