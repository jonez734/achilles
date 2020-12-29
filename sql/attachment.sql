create table achilles.__attachment (
  "id" serial unique not null primary key,
  "fooditemid" integer constraint fk_attachment_fooditemid references achilles.__fooditem(id) on update cascade on delete set null,
  "label" text,
  "description" text,
  "filepath" text not null,
  "mimetype" text not null,
  "dateposted" timestamptz,
  "postedbyid" integer constraint fk_attachment_postedbyid references engine.__member(id) on update cascade on delete set null,
  "datemodified" timestamptz,
  "modifiedbyid" integer constraint fk_attachment_modifiedbyid references engine.__member(id) on update cascade on delete set null,
  "dateapproved" timestamptz,
  "approvedbyid" integer constraint fk_attachment_approvedbyid references engine.__member(id) on update cascade on delete set null
);

grant insert, update, delete on achilles.__attachment to "apache";

create view achilles.attachment as 
  select 
    achilles.__attachment.*, 
    extract(epoch from achilles.__attachment.datemodified) as datemodifiedepoch,
    extract(epoch from achilles.__attachment.dateapproved) as dateapproved epoch,
    extract(epoch from achilles.__attachment.dateposted) as datepostedepoch
  from achilles.__attachment
;

grant select on achilles.attachment to "apache";
