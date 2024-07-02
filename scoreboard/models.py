from django.db import models

from player.models import Player
from tournament.models import Tournament


# Create your models here.

class Scoreboard(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, related_name='scoreboard')


class ScoreboardPlayer(models.Model):
    scoreboard = models.ForeignKey(Scoreboard, on_delete=models.CASCADE, related_name='scoreboard_players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scoreboards')
    rank = models.PositiveSmallIntegerField()