"""Module for generating events by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from gameraterreports.views.helpers import dict_fetch_all


class TopReviewersList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            db_cursor.execute("""
            select user.first_name || " " || user.last_name as full_name, count(review.id) as num_reviews from gameraterapi_player player
            left join gameraterapi_gamereview review on review.player_id = player.id
            join auth_user user on user.id = player.user_id
            group by full_name
            order by num_reviews desc
            limit 3
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)


            top_3_reviewers = []

            for row in dataset:

                if row['num_reviews'] is not None:
                    player = {
                        "name": row['full_name'],
                        "num_reviews": row['num_reviews'],
                    }
                else:
                    player = {
                        "name": row['full_name'],
                        "num_reviews": 0,
                    }
                
                top_3_reviewers.append(player)
                
        
        # The template string must match the file name of the html template
        template = 'players/list_of_top_3_reviewers.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "topreviewers_list": top_3_reviewers
        }

        return render(request, template, context)
