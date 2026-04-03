create table if not exists achilles.map_fooditem_additive (
    fooditemid bigint not null constraint fk_map_fooditem_fooditem references engine.__node(id) on update cascade on delete cascade,
    result text
);

grant all on achilles.map_fooditem_additive to :web;
grant all on achilles.map_fooditem_additive to :bbs;
