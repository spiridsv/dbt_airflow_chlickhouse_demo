
-- Use the `ref` function to select from other models

select 1 as z
     , gender
--      , -1 as cnt
     , count() as cnt
from {{ ref('my_first_dbt_model') }}
group by 1,2
