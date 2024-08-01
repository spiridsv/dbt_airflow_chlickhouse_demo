{{ config(materialized='table') }}

with
    extract_actors as (
        select
            id, name, -- TEST RELATIONSHIP
            actors, roles,
            arrayJoin(actors) as actor_id
        from {{ ref('roles_in_movie') }}
    )
-- select 1 as id from extract_actors a
select * from extract_actors a
         left join {{ ref('my_first_dbt_model') }} b on a.actor_id = b.id
