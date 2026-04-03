\echo vendor
create table achilles.__vendor (
    type text,
    name text,
    qsr boolean,
    chain boolean,
    independentlyowned boolean,
    independentlyoperatated boolean,
    url text
);

create or replace view achilles.vendor as
    select 
        n.*,
        (n.attributes->>'type')::text,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'qsr')::boolean as qsr,
        (n.attributes->>'chain')::boolean as chain,
        (n.attributes->>'independentlyowned')::boolean as independentlyowned,
        (n.attributes->>'independentlyoperated')::boolean as independentlyoperated,
        (n.attributes->>'url')::text as url
    from engine.node as n
    where n.prg = 'achilles.vendor'
;

grant select on achilles.vendor to :web;
grant select on achilles.vendor to :bbs;
