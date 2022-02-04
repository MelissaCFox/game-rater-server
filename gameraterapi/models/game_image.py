from django.db import models

class GameImage(models.Model):
    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name='images')
    player = models.ForeignKey("Player", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gameimages', height_field=None, 
                              width_field=None, max_length=100, null=True)
