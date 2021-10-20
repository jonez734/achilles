create or replace view achilles.equipment as
    select n.*,
        (n.attributes->>'type')::text as type,
        (n.attributes->>'make')::text as make,
        (n.attributes->>'model')::text as model,
        (n.attributes->>'year')::text as year,
    from engine.node as n
    where n.prg='achilles.equipment'
;

create or replace table achilles.map_lab_equipment(
    labid bigint,
    equipmentid bigint
);

grant all on achilles.map_lab_equipment to 'apache';
