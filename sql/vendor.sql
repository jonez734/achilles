create view vendor as
    select 
        *,
        (attributes->>'name')::text as name,
        (attributes->>'qsr')::boolean as qsr,
        (attributes->>'chain')::boolean as chain,
        (attributes->>'independentlyowned'::boolean as independentlyowned,
        (attributes->>'independentlyoperated'::boolean as independentlyoperated,
        (attributes->>'url')::text as url
    from engine.node
    where attributes ? 'name' and attributes ? 'qsr' and attributes ? 'url' and attributes ? 'chain' and attributes ? 'independentlyowned' and attributes ? 'independentlyoperated'
;
