\echo manuf
create or replace view achilles.manuf as
    select n.*,
        (n.attributes->>'ownerid')::bigint as ownerid,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'title')::text as title
    from engine.node as n
    where n.prg = 'achilles.manuf'
;

