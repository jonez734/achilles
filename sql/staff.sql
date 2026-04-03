create or replace view achilles.staff as
    select b.*,
    (attributes->>'datehired')::timestamptz,
    (attributes->>'credentials')::text
    from engine.__blurb
    where prg='achilles.staff'
;

grant select on achilles.staff to :web;
grant select on achilles.staff to :bbs;
