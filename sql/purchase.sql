\echo purchase
create or replace view purchase as
    select n.*,
        (n.attributes->>'merchantid')::bigint as merchantid,
        (n.attributes->>'vendorid')::bigint as vendorid,
        (n.attributes->>'fooditemid')::bigint as fooditemid,
        (n.attributes->>'price')::numeric(10,2) as price,
        (n.attributes->>'datepurchased')::timestamptz as datepurchased
    from engine.node as n
    where n.prg = 'achilles.purchase'
;
