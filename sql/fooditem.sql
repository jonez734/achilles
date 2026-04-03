\echo fooditem
create or replace view achilles.fooditem as
  select b.*,
    (b.attributes->>'brandid')::bigint as brandid,
    (b.attributes->>'manufid')::bigint as manufid,
    (b.attributes->>'upc')::text as upc,
    (b.attributes->>'sku')::text as sku,
    (b.attributes->>'lot')::text as lot,
    (b.attributes->>'serial')::text as serial,
    (b.attributes->>'name')::text as name,
    (b.attributes->>'title')::text as title,
    (b.attributes->>'description')::text as description,
    (b.attributes->>'frozen')::boolean as frozen,
    (b.attributes->>'wic')::boolean as wic
  from engine.__blurb as b
  where b.prg = 'achilles.fooditem'
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
