select  id,
        concat(first_name, ' ', last_name) as actor,
       groupArray(distinct rols.role) as roles,
       length(roles) as roles_count
    from {{ source('imdb', 'actors') }} as act
    left join {{ source('imdb', 'roles') }} as rols on act.id = rols.actor_id
    group by 1,2
