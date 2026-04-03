\echo purchase
create table __purchase (
    merchantid bigint
);

create or replace view purchase as
    
    select b.*,
        (b.attributes->>'merchantid')::bigint as merchantid,
        (b.attributes->>'vendorid')::bigint as vendorid,
        (b.attributes->>'fooditemid')::bigint as fooditemid,
        (b.attributes->>'price')::numeric(10,2) as price,
        (b.attributes->>'datepurchased')::timestamptz as datepurchased
    from engine.__blurb as b
    where b.prg = 'achilles.purchase'
;
