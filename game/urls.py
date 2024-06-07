from django.urls import path

from game.views import update_game

urlpatterns=[
    path('<int:pk>/update_game/', update_game, name='update_game'),
]