from django.urls import path

from game.views import update_game
from step.views import create_second_step

urlpatterns = [
    path('<int:pk>/update_game/', update_game, name='update_game'),
]
