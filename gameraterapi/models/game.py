from django.db import models

class Game(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    designer = models.CharField(max_length=50)
    year_released = models.PositiveIntegerField()
    number_of_players = models.PositiveIntegerField()
    est_playtime = models.PositiveIntegerField()
    age_recommendation = models.PositiveBigIntegerField()
    average_rating = models.FloatField()
    ## Need to learn how to make average_rating property an aggregate of game ratings

    categories = models.ManyToManyField("Category", through="GameCategory", related_name="games")

    # ratings = []
    # reviews = []
    # images = []

    ## categories =
    ## ratings =
    ## reviews =
    ## images =
