from django.db import models

from tournament.models import Tournament


# Create your models here.
class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    points = models.IntegerField(default=0)
    tournaments = models.ManyToManyField(Tournament, related_name='players')

    def __str__(self):
        return f'{self.first_name} {self.last_name} with id {self.pk}'