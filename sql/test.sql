create or replace view achilles.test as
    select n.*,
        (n.attributes->>'fooditemid')::bigint as fooditemid,
        (n.attributes->>'labid')::bigint as labid,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'testedbyid')::bigint as testedbyid,
        (n.attributes->>'datetested')::timestamptz as datetested,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'result')::text as result
    from engine.node as n
    where n.prg='achilles.test'
;
