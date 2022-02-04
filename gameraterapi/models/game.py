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
    # average_rating = models.FloatField()
    ## Need to learn how to make average_rating property an aggregate of game ratings

    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")

    @property
    def average_rating(self):
        """Average rating calculated attribute for each game"""
        ratings = GameRating.objects.filter(game=self)

        # Sum all of the ratings for the game
        total_rating = 0
        for rating in ratings:
            total_rating += rating.rating
            
        average_rating = total_rating / len(ratings)
        return average_rating

    # Calculate the averge and return it.
    # If you don't know how to calculate averge, Google it.

    # ratings = []
    # reviews = []
    # images = []

    ## categories =
    ## ratings =
    ## reviews =
    ## images =
