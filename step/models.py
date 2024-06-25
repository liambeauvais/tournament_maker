from django.db import models

from player.models import Player
from tournament.models import Tournament


# Create your models here.
class Step(models.Model):
    last_step = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name="steps")
    rank = models.IntegerField(default=0)

    def is_done(self):
        return all(pool.validated for pool in self.pools.all())



