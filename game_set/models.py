from django.db import models

from game.models import Game


# Create your models here.
class Set(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sets')
    score = models.IntegerField(null=True, blank=True)
    number = models.IntegerField()
