from django.apps import AppConfig


class GameSetConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game_set'

    def ready(self):
        from .signals import set_updated
        super().ready()
