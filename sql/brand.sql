\echo brand
create or replace view achilles.brand as
    select b.*,
        (b.attributes->>'manufid')::bigint as manufid,
        (b.attributes->>'name') as name,
        (b.attributes->>'url') as url,
        (b.attributes->>'ownerid')::bigint as ownerid
    from engine.__blurb as b
    where b.prg = 'achilles.brand'
;

grant select on achilles.brand to :web;
grant select on achilles.brand to :bbs;
