from django.urls import path

from scoreboard.views import ScoreBoardView, create_scoreboard
from step.views import create_first_step, StepView, SecondStepsView, create_final_steps, FinalStepsView, \
    create_second_step
from tournament.views import TournamentView, TournamentDetailView, add_player_to_tournament, \
    delete_player_from_tournament, pdf_view

urlpatterns = [
    path('', TournamentView.as_view(), name='tournaments'),
    path('<int:pk>/', TournamentDetailView.as_view(), name='tournament_detail'),
    path('<int:pk>/add_player/<int:player_id>/', add_player_to_tournament, name='add_player_to_tournament'),
    path('<int:pk>/delete_player_from_tournament/<int:player_id>/', delete_player_from_tournament,
         name='delete_player_from_tournament'),
    path('<int:pk>/create_first_step/', create_first_step, name='create_first_step'),
    path('<int:pk>/create_second_steps/', create_second_step, name='create_second_step'),
    path('<int:pk>/create_final_steps/', create_final_steps, name='create_final_steps'),

    path('<int:pk>/steps/', StepView.as_view(), name='steps'),
    path('<int:pk>/second_steps/', SecondStepsView.as_view(), name='second_steps'),
    path('<int:pk>/final_steps/', FinalStepsView.as_view(), name='final_steps'),

    path('<int:pk>/create_scoreboard/', create_scoreboard, name='create_scoreboard'),
    path('<int:pk>/scoreboard/', ScoreBoardView.as_view(), name='scoreboard'),
    path("<int:step_pk>/pdf/<int:step_iteration>", pdf_view, name='step_pdf'),
    path("pdf/", pdf_view, name='step_pdf'),

]

