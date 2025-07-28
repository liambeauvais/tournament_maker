from django.urls import path

from pool.views import modify_table, remove_player_from_pool

urlpatterns = [
    path('<int:pk>/modify_table/', modify_table, name='modify_table'),
    path('remove_player_from_pool/', remove_player_from_pool, name='remove_player_from_pool')
]
