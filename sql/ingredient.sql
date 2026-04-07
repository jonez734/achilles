\echo ingredient
create or replace view achilles.ingredient as 
    select b.*,
        (b.attributes->>'type')::text as type,
        (b.attributes->>'name')::text as name,
        (b.attributes->>'quantity')::text as quantity,
        (b.attributes->>'offlabel')::boolean as offlabel,
--        (b.attributes->>'additive')::boolean as additive ?
    from engine.__blurb as b
    where b.prg='achilles.ingredient'
;

grant select on achilles.ingredient to :web;
grant select on achilles.ingredient to :bbs;

create table if not exists achilles.map_fooditem_ingredient (
    fooditemid bigint not null constraint fk_map_fooditem_fooditem references engine.__blurb(id) on update cascade on delete cascade,
    ingredientid bigint not null constraint fk_map_fooditem_ingredient references engine.__blurb(id) on update cascade on delete cascade
);

create unique index if not exists idx_map_fooditem_ingredient on achilles.map_fooditem_ingredient(fooditemid, ingredientid);

grant all on achilles.map_fooditem_ingredient to :web;
grant all on achilles.map_fooditem_ingredient to :bbs;
