
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with source_data_id as (
    select id, gender from {{ source('imdb', 'actors') }}
)

select id, id+1000 as myid, gender
from source_data_id

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
