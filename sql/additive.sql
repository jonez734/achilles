create view achilles.additive as
    select n.*,
        (n.attributes->>'title')::text as title,
        (n.attributes->>'description')::text as description
    from engine.node as n
    where (n.attributes->>'prg')::text = 'achilles.additive'
;

create table achilles.map_fooditem_additives (
    fooditemid bigint constraint fk_fooditem_additive references achilles.fooditem(id) on update cascade on delete cascade
);
