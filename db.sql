select user.first_name || " " || user.last_name as full_name, count(review.id) as num_reviews from gameraterapi_player player
left join gameraterapi_gamereview review on review.player_id = player.id
join auth_user user on user.id = player.user_id
group by full_name
order by num_reviews desc
limit 3