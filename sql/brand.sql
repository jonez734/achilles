create or replace view achilles.brand as
    select n.*,
        (n.attributes->>'manufid')::bigint as manufid,
        (n.attributes->>'name') as name,
        (n.attributes->>'url') as url,
        (n.attributes->>'ownerid')::bigint as ownerid
    from engine.node as n
    where n.prg = 'achilles.brand'
;
