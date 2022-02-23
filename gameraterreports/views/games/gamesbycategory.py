from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class CategoryGameCountList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select category.label, count(game_id) as num_games from gameraterapi_category category
            left join gameraterapi_gamecategory game on game.category_id = category.id
            group by category.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            categories = []

            for row in dataset:

                if row['num_games'] is not None:
                    category = {
                        "label": row['label'],
                        "num_games": row['num_games'],
                    }
                else:
                    category = {
                        "label": row['label'],
                        "num_games": 0,
                    }
                
                categories.append(category)
                
        
        # The template string must match the file name of the html template
        template = 'games/category_game_count.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "categorygamecount_list": categories
        }

        return render(request, template, context)
