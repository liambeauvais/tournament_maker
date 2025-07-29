from django.urls import path

from pool.views import modify_table, remove_player_from_pool, add_player

urlpatterns = [
    path('<int:pk>/modify_table/', modify_table, name='modify_table'),
    path('<int:pk>/add_player/', add_player, name='add_player'),
    path('remove_player_from_pool/', remove_player_from_pool, name='remove_player_from_pool')
]
