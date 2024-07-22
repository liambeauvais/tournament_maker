from django.db import models

from player.models import Player
from step.models import Step


# Create your models here.
class Pool(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="pools")
    validated = models.BooleanField(default=False)

    def is_done(self):
        return all(game.winner is not None for game in self.games.all())


class PoolPLayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pools')
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name='players')
    rank = models.IntegerField(default=0)
    coeff = models.FloatField(default=0)
