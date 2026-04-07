\echo corp
create or replace view achilles.corp as
    select n.*,
        (n.attributes->>'type') as type,
        (n.attributes->>'name') as name,
        (n.attributes->>'title') as title,
        (n.attributes->>'url') as url
    from engine.node as n
    where n.prg = 'achilles.corp'
;

grant select on achilles.corp to :web;
grant select on achilles.corp to :bbs;
