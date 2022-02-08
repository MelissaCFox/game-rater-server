from django.db import models
from django.contrib.auth.models import User
from gameraterapi.models.player import Player

class GameReview(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="reviews")
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='author')
    review = models.TextField()
    date_time = models.DateTimeField()


    # custom 'author' property (with getter and setter) that returns a boolean
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, value):
        self.__author = value
            