create table achilles.__merchant (
    "id" serial unqiue not null primary key,
    "name" text unique,
    "type" text,
    "qsr" boolean default 'f',
    "datecreated" timestamptz,
    "createdbyid" integer  constraint fk_seller_createdbyid references engine.__member(id) on update cascade on delete set null,
    "datemodified" timestamptz,
    "modifiedbyid" integer constraint fk_fooditem_modifiedbyid references engine.__member(id) on update cascade on delete set null
);
