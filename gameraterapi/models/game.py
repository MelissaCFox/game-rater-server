from django.db import models

from gameraterapi.models.game_rating import GameRating

class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    est_playtime = models.PositiveIntegerField()
    age_recommendation = models.PositiveBigIntegerField()
    player = models.ForeignKey("Player", on_delete=models.CASCADE)


    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        if len(ratings) > 0:
            for rating in ratings:
                total_rating += rating.rating
                
            average_rating = total_rating / len(ratings)
            rounded_average = round(average_rating, 1)
            return rounded_average
        else:
            return "No Ratings Yet"

    # reviews = []
    # images = []
