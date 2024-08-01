select id, a.gender, b.cnt
from {{ ref('my_first_dbt_model') }} as a
    left join {{ ref('my_second_dbt_model') }} as b on a.gender = b.gender
