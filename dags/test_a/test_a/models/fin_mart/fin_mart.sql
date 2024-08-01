{{ config(materialized='table', order_by='id', partition_by='y.gender') }}

select *
     , length(actors)
     , length(roles)
from {{ ref('mart2') }} x
         left join {{ ref('my_mart') }} y on x.actor_id = y.id
