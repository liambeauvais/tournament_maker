from django.db import models

from tournament.models import Tournament


# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    tournaments = models.ManyToManyField(Tournament, related_name='players')
