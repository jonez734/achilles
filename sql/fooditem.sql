\echo fooditem
create table if not exists achilles.__fooditem (
    "id" bigserial unique not null primary key,
    "upc" text,
    "sku" text,
    "lot" text,
    "serial" text,
    "name" text not null,
    "title" text,
    "description" text,
    "brandid" bigint,
    "manufid" bigint,
    "qsr" boolean default false,
    "msgpresent" boolean default false,
    "msgonlabel" boolean default false,
    "dsgpresent" boolean default false,
    "dsgonlabel" boolean default false,
    "frozen" boolean default false,
    "wic" boolean default false,
    "price" numeric(10,2),
    "quantity" text,
    "producturl" text,
    "datepurchased" timestamptz,
    "dateposted" timestamptz,
    "postedbymoniker" citext constraint fk_fooditem_postedbymoniker references engine.__member(moniker) on update cascade on delete set null,
    "datemodified" timestamptz,
    "modifiedbymoniker" citext constraint fk_fooditem_modifiedbymoniker references engine.__member(moniker) on update cascade on delete set null
);

create unique index if not exists idx_fooditem_upc on achilles.__fooditem(upc) where upc is not null;
create unique index if not exists idx_fooditem_name on achilles.__fooditem(name) where name is not null;

grant insert, update, delete on achilles.__fooditem to :web;
grant select on achilles.__fooditem to :web;
grant select on achilles.__fooditem to :bbs;

create or replace view achilles.fooditem as
  select
    id,
    upc,
    sku,
    lot,
    serial,
    name,
    title,
    description,
    brandid,
    manufid,
    qsr,
    msgpresent,
    msgonlabel,
    dsgpresent,
    dsgonlabel,
    frozen,
    wic,
    price,
    quantity,
    producturl,
    datepurchased,
    dateposted,
    postedbymoniker,
    datemodified,
    modifiedbymoniker,
    extract(epoch from datepurchased) as datepurchasedepoch,
    extract(epoch from dateposted) as datepostedepoch,
    extract(epoch from datemodified) as datemodifiedepoch
  from achilles.__fooditem
;

grant select on achilles.fooditem to :web;
grant select on achilles.fooditem to :bbs;
