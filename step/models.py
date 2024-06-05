from django.db import models

from tournament.models import Tournament


# Create your models here.
class Step(models.Model):
    last_step = models.ForeignKey('self', on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)