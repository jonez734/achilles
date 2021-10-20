create or replace view achilles.lab as
    select n.*,
        (n.attributes->>'type') as type,
        (n.attributes->>'name') as name,
        (n.attributes->>'title') as title,
        (n.attributes->>'address') as address
    from engine.node as n
    where n.prg='achilles.lab'
;
