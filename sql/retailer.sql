create view retailer as
    select 
        *,
        (attributes->>'name')::text as name,
        (attributes->>'qsr')::boolean as qsr,
        (attributes->>'url')::text as url
    from engine.node
    where attributes ? 'name' and attributes ? 'qsr' and attributes ? 'url'
;
