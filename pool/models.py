from django.db import models

from game.models import Game
from player.models import Player
from step.models import Step


# Create your models here.
class Pool(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game, related_name='pools')
    players = models.ManyToManyField(Player, related_name='pools')
    validated = models.BooleanField(default=False)

    def is_done(self):
        print(all(game.winner is not None for game in self.games.all()))
        return all(game.winner is not None for game in self.games.all())
