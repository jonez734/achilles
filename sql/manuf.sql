create or replaces view manuf as
    select n.*,
        (n.attributes->>'ownerid')::bigint as ownerid, -- corp
        (n.attributes->>'name')::text as name,
        (n.attributes->>'title')::text as title
    from engine.node as n
    where n.prg = 'achilles.manuf'
;

