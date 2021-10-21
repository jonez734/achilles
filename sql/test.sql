\echo test
create or replace view achilles.test as
    select n.*,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'name')::text as name
    from engine.node as n
    where n.prg='achilles.test'
;

create table if not exists achilles.map_fooditem_test (
    fooditemid bigint not null constraint fk_map_fooditem_fooditem references engine.__node(id) on update cascade on delete cascade,
    labid bigint not null constraint fk_map_fooditem_labid references engine.__node(id) on update cascade on delete cascade,
    testid bigint not null constraint fk_map_fooditem_test references engine.__node(id) on update cascade on delete cascade,
    testedbyid bigint not null constraint fk_map_fooditem_testedbyid references engine.member(id) on update cascade on delete set null,
    datetested timestamptz,
    result text
);
