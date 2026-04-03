\echo test
create or replace view achilles.test as
    select b.*,
        (b.attributes->>'type')::text as type,
        (b.attributes->>'name')::text as name
    from engine.__blurb as b
    where b.prg='achilles.test'
;

grant select on achilles.test to :web;
grant select on achilles.test to :bbs;

create table if not exists achilles.map_fooditem_test (
    fooditemid bigint not null constraint fk_map_fooditem_fooditem references engine.__blurb(id) on update cascade on delete cascade,
    labid bigint not null constraint fk_map_fooditem_labid references engine.__blurb(id) on update cascade on delete cascade,
    testid bigint not null constraint fk_map_fooditem_test references engine.__blurb(id) on update cascade on delete cascade,
    testedbyid bigint not null constraint fk_map_fooditem_testedbyid references engine.__member(id) on update cascade on delete set null,
    datetested timestamptz,
    result text
);

grant all on achilles.map_fooditem_test to :web;
grant all on achilles.map_fooditem_test to :bbs;
