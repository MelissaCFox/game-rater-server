from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class MostReviewedGame(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select game.title, count(game_id) as num_reviews from gameraterapi_game game
            left join gameraterapi_gamereview review on review.game_id = game.id
            group by game.id
            order by num_reviews desc
            limit 1
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            games = []

            for row in dataset:

                game = {
                    "title": row['title'],
                    "num_reviews": row['num_reviews'],
                    }
                
                games.append(game)
                
        
        # The template string must match the file name of the html template
        template = 'games/most_reviewed_game.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "mostreviewedgame_list": games
        }

        return render(request, template, context)
