\echo purchase
create table if not exists achilles.__purchase (
    "id" bigserial unique not null primary key,
    "merchantid" bigint,
    "vendorid" bigint,
    "fooditemid" bigint,
    "price" numeric(10,2),
    "datepurchased" timestamptz,
    "dateposted" timestamptz,
    "postedbymoniker" citext constraint fk_purchase_postedbymoniker references engine.__member(moniker) on update cascade on delete set null,
    "datemodified" timestamptz,
    "modifiedbymoniker" citext constraint fk_purchase_modifiedbymoniker references engine.__member(moniker) on update cascade on delete set null
);

grant insert, update, delete on achilles.__purchase to :web;
grant select on achilles.__purchase to :web;
grant select on achilles.__purchase to :bbs;

create or replace view achilles.purchase as
  select
    id,
    merchantid,
    vendorid,
    fooditemid,
    price,
    datepurchased,
    dateposted,
    postedbymoniker,
    datemodified,
    modifiedbymoniker,
    extract(epoch from datepurchased) as datepurchasedepoch,
    extract(epoch from dateposted) as datepostedepoch,
    extract(epoch from datemodified) as datemodifiedepoch
  from achilles.__purchase
;

grant select on achilles.purchase to :web;
grant select on achilles.purchase to :bbs;
