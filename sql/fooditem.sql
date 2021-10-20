create or replace view achilles.fooditem as
  select n.*,
    (n.attributes->>'brandid')::bigint as brandid,
    (n.attributes->>'manufid')::bigint as manufid,
    (n.attributes->>'upc')::text as upc,
    (n.attributes->>'sku')::text as sku,
    (n.attributes->>'name')::text as name,
    (n.attributes->>'title')::text as title,
    (n.attributes->>'ingredients') as ingredients,
    (n.attributes->>'description')::text as description,
--    (n.attributes->>'testedbyid') as testedbyid,
--    (n.attributes->>'datetested') as datetested,
    (n.attributes->>'frozen')::boolean as frozen
  from engine.node as n
  where n.prg = 'achilles.fooditem'
;

--create table achilles.__fooditem (
--  "id" serial unique not null primary key,
--  "upc" text unique,
--  "name" text,
--  "description" text,
--  "brand" text,
--  "industry" text, -- fast food (qsr), hospitality, etc
--  "frozen" boolean default 'f',
--  "price" numeric(10,2),
--  "msgpresent" boolean default 'f',
--  "msgonlabel" boolean default 'f',
--  "dsgpresent" boolean default 'f',
--  "dsgonlabel" boolean default 'f',
--  "quantity" text,
--  "producturl" text,
--  "storeid" text,
--  "locationpurchased" text,
--  "datepurchased" timestamptz,
--  "postedbyid" integer constraint fk_fooditem_postedbyid references engine.__member(id) on update cascade on delete set null,
--  "dateposted" timestamptz,
--  "datemodified" timestamptz,
--  "modifiedbyid" integer constraint fk_fooditem_modifiedbyid references engine.__member(id) on update cascade on delete set null
--);

--grant insert, update, delete on achilles.__fooditem to "apache";

--create view achilles.fooditem as
--  select achilles.__fooditem.*,
--    extract(epoch from datepurchased) as datepurchasedepoch,
--    extract(epoch from dateposted) as datepostedepoch,
--    extract(epoch from datemodified) as datemodifiedepoch
--  from achilles.__fooditem
--;

--grant select on achilles.fooditem to "apache";
