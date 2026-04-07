\echo additive
create or replace view achilles.additive as
    select n.*,
        attributes->>'title' as title,
        attributes->>'shortname' as shortname
    from engine.__node
    where n.prg = 'achilles.additive'
;

grant select on achilles.additive to :web;
grant select on achilles.additive to :bbs;
