from django.urls import path

from step.views import validate_pool, force_pool_validation

urlpatterns = [
    path('<int:pk>/validate_pool/<int:pool_pk>', validate_pool, name='validate_pool'),
    path('<int:pk>/force_pool_validation/<int:pool_pk>/', force_pool_validation, name='force_pool_validation'),
]
