from django.apps import AppConfig


class GrafanausermanagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GrafanaUserManag'

    def ready(self):
        import GrafanaUserManag.signals
