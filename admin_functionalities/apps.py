from django.apps import AppConfig


class AdminFunctionalitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_functionalities"
    
    def ready(self):
        import admin_functionalities.signals
