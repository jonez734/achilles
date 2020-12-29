create table achilles.__fooditem (
  "id" serial unique not null primary key,
  "upc" text unique,
  "name" text,
  "description" text,
  "brand" text,
  "qsr" boolean default 'f',
  "price" numeric(10,2),
  "msgpresent" boolean default 'f',
  "msgonlabel" boolean default 'f',
  "msgquantity" text,
  "locationpurchased" text,
  "datepurchased" timestamptz,
  "postedbyid" integer constraint fk_fooditem_postedbyid references engine.__member(id) on update cascade on delete set null,
  "dateposted" timestamptz,
  "datemodified" timestamptz,
  "modifiedbyid" integer constraint fk_fooditem_modifiedbyid references engine.__member(id) on update cascade on delete set null
);

grant insert, update, delete on achilles.__fooditem to "apache";

create view achilles.fooditem as
  select achilles.__fooditem.*,
    extract(epoch from datepurchased) as datepurchasedepoch,
    extract(epoch from dateposted) as datepostedepoch,
    extract(epoch from datemodified) as datemodifiedepoch
  from achilles.__fooditem
;

grant select on achilles.fooditem to "apache";
