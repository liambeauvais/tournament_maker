from django.db import models

from player.models import Player
from tournament.models import Tournament


# Create your models here.
class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, related_name='games', null=True)
    player_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_one')
    player_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_two')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="wins", null=True)
