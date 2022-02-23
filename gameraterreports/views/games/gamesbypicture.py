from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class NoPictureGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select * from gameraterapi_game game
            left join gameraterapi_gameimage i on i.game_id = game.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            games = []

            for row in dataset:
                if row['image'] is None:
                    game = {
                        "title": row['title'],
                        }
                    
                    games.append(game)
                
        
        # The template string must match the file name of the html template
        template = 'games/no_picture_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "nopicturegames_list": games
        }

        return render(request, template, context)
