from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class CategoryGamesForChildrenList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select * from gameraterapi_category category
            join gameraterapi_gamecategory gc on gc.category_id = category.id
            join gameraterapi_game game on gc.game_id = game.id
            where game.age_recommendation <= 8
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            categories = []

            for row in dataset:

                game = {
                    "title": row['title'],
                    'age_recommendation': row['age_recommendation']
                    }
                
                category_dict = next(
                    (
                        category_game for category_game in categories
                        if category_game['category_id'] == row['category_id']
                    ),
                    None
                )
                
                if category_dict:
                    category_dict['games'].append(game)
                else:
                    categories.append({
                        'category_id': row['category_id'],
                        'label': row['label'],
                        'games': [game]
                    })


        # The template string must match the file name of the html template
        template = 'games/category_games_for_children.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "categorykidsgames_list": categories
        }

        return render(request, template, context)
