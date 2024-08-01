{{ config(materialized='table') }}

select id, name, groupArray(actor_id) as actors, groupArrayDistinct(role) as roles
from {{ source('imdb', 'movies') }} a
    left join {{ source('imdb', 'roles') }} b on a.id = b.movie_id
group by 1,2