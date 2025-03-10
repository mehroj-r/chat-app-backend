from django.apps import AppConfig


class ChatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_app'

    def ready(self):
        import chat_app.signals