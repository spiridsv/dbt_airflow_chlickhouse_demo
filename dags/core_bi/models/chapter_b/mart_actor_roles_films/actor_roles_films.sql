select actor,
       groupArray(distinct flms.name) as movies,
       length(movies) as movies_count,
       groupArray(distinct flms.id) as movies_id,
       length(movies_id) as movies_id_count
    from {{ ref('actor_roles') }} as act
    left join {{ source('imdb', 'roles') }} as rols on act.id = rols.actor_id
    left join {{ source('imdb', 'movies') }} as flms on rols.movie_id = flms.id
    group by 1
