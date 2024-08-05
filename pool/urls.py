from django.urls import path

from pool.views import modify_table

urlpatterns = [
    path('<int:pk>/modify_table/', modify_table, name='modify_table')
]
