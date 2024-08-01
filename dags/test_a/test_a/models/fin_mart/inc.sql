{{
    config(
    materialized='table',
    incremental_strategy='delete+insert',
    order_by='id',
    unique_key='id'
    )
}}

select id, count(id)
from {{ ref('fin_mart') }}
group by 1