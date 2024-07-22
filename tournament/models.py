from django.db import models

CATEGORIES = [
    ("L", "Loisir"),
    ("J", "Jeunes"),
    ("C", "Compétiteurs")
]

TOURNAMENT_TYPES = [
    ("RONDE", 'Rondes'),
    ("CLASSIC", "Classique")
]


# Create your models here.
class Tournament(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES, default="C")
    closed = models.BooleanField(default=False)
    tournament_type = models.CharField(max_length=100, choices=TOURNAMENT_TYPES, default="CLASSIC")

    def __str__(self):
        return f"{self.name}"