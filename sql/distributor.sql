--
-- used for food distributors like "GFS"
--

\echo distributor
create or replace view achilles.distributor as
    select 
        n.*,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'independentlyowned')::boolean as independentlyowned,
        (n.attributes->>'independentlyoperated')::boolean as independentlyoperated,
        (n.attributes->>'url')::text as url,
        (n.attributes->>'nationwide')::boolean as nationwide,
        (n.attributes->>'worldwide')::boolean as worldwide,
        (n.attributes->>'nation')::text as nation
    from engine.node as n
    where n.prg = 'achilles.distributor'
;
