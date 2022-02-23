select * from gameraterapi_category category
join gameraterapi_gamecategory gc on gc.category_id = category.id
join gameraterapi_game game on gc.game_id = game.id
where game.age_recommendation <= 8


