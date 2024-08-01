select gender, count() as cnt
from {{ source('imdb', 'actors') }}
group by 1
