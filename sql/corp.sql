create or replace view achilles.corp as
    select n.*,
        (n.attributes->>'name') as name,
        (n.attributes->>'title') as title
    from engine.node as n
    where n.prg = 'achilles.corp'
;
