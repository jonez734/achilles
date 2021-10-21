\echo ingredient
create or replace view achilles.ingredient as 
    select n.*,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'name')::text as name,
        (n.attributes->>'quantity')::text as quantity
    from engine.node as n
    where n.prg='achilles.ingredient'
;

create table if not exists achilles.map_fooditem_ingredient (
    fooditemid bigint not null constraint fk_map_fooditem_fooditem references engine.__node(id) on update cascade on delete cascade,
    ingredientid bigint not null constraint fk_map_fooditem_ingredient references engine.__node(id) on update cascade on delete cascade
);

create unique index if not exists idx_map_fooditem_ingredient on achilles.map_fooditem_ingredient(fooditemid, ingredientid);
