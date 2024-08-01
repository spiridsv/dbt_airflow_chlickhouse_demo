select actor,
       roles,
       movies
    from {{ ref('actor_roles') }} as a
    left join {{ ref('actor_roles_films')  }} as b using(actor)
