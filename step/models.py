from django.db import models

from player.models import Player
from tournament.models import Tournament


# Create your models here.
class Step(models.Model):
    last_step = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class StepPLayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="steps")
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="players")
    rank = models.IntegerField(default=0)
