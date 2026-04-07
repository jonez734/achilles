create or replace view achilles.equipment as
    select n.*,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'make')::text as make,
        (n.attributes->>'model')::text as model,
        (n.attributes->>'year')::text as year
    from engine.node as n
    where n.prg='achilles.equipment'
;

grant select on achilles.equipment to :web;
grant select on achilles.equipment to :bbs;

create table if not exists achilles.map_lab_equipment(
    labid bigint constraint fk_map_lab_equipment_labid references engine.__node(id) on update cascade on delete cascade,
    equipmentid bigint constraint fk_map_lab_equipment_equipmentid references engine.__node(id) on update cascade on delete cascade,
    equipmentserialnumber text,
    dateinstalled timestamptz
);

grant all on achilles.map_lab_equipment to :web;
grant all on achilles.map_lab_equipment to :bbs;

grant all on achilles.map_lab_equipment to :web;
grant all on achilles.map_lab_equipment to :bbs;
