from django.db import models

class GameReview(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="reviews")
    player = models.ForeignKey("Player", on_delete=models.CASCADE, related_name='author')
    review = models.TextField()
    date_time = models.DateTimeField()
