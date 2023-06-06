from django.apps import AppConfig


class PeliculasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Peliculas'

class EventiketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Eventiket'

    def ready(self):
        import Eventiket.templatetags.custom_filters