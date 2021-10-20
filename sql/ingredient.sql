create or replace view achilles.ingredient as 
    select n.*,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'quantity')::text as quantity
    from engine.node as n
    where n.prg='achilles.ingredient'
;
