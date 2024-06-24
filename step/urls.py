from django.urls import path

from step.views import validate_pool

urlpatterns = [
    path('<int:pk>/validate_pool/<int:pool_pk>', validate_pool, name='validate_pool')
]