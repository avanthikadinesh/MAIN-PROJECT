from django.apps import AppConfig

class PersonalAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personal_app'

    def ready(self):
        import personal_app.signals

