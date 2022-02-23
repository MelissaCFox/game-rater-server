"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class BottomGamesList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select game.title, round(avg(rating),2) as average_rating from gameraterapi_game game
            left join gameraterapi_gamerating r on r.game_id = game.id
            group by game.id
            order by average_rating
            limit 5
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            bottom_five_rated_games = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the game title and average ratingfrom the row dictionary
                if row['average_rating'] is not None:
                    game = {
                        "title": row['title'],
                        "average_rating": row['average_rating'],
                    }
                else:
                    game = {
                        "title": row['title'],
                        "average_rating": "N/A",
                    }
                
                bottom_five_rated_games.append(game)
                
        
        # The template string must match the file name of the html template
        template = 'games/list_of_bottom_5_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "bottomgames_list": bottom_five_rated_games
        }

        return render(request, template, context)
