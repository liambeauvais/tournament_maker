from django.db import models

from player.models import Player
from pool.models import Pool
from tournament.models import Tournament


# Create your models here.
class Game(models.Model):
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='games', null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='games', null=True)
    player_one = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_one')
    player_two = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='games_as_two')
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="wins", null=True)
