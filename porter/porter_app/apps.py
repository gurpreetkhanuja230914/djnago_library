from django.apps import AppConfig


class PorterAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'porter_app'
    def ready(self):
        import porter_app.signals
