from django.urls import path

from step.views import create_first_step
from tournament.views import TournamentView, TournamentDetailView, add_player_to_tournament, \
    delete_player_from_tournament

urlpatterns = [
    path('', TournamentView.as_view(), name='tournaments'),
    path('<int:pk>/', TournamentDetailView.as_view(), name='tournament_detail'),
    path('<int:pk>/add_player/<int:player_id>/', add_player_to_tournament, name='add_player_to_tournament'),
    path('<int:pk>/delete_player_from_tournament/<int:player_id>/', delete_player_from_tournament,
         name='delete_player_from_tournament'),
    path('<int:pk>/create_first_step', create_first_step, name='create_first_step')
]
