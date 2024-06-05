from django.db import models

TYPES = [
    ("L", "Loisir"),
    ("J", "Jeunes"),
    ("C", "Compétiteurs")
]


# Create your models here.
class Tournament(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    set_number = models.IntegerField(default=5)
    type = models.CharField(max_length=100, choices=TYPES, default="C")
