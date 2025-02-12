from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_app'

    def ready(self):
        """
        This method is called when the Django application is ready.
        It imports the signals module from the user_app.api package,
        ensuring that the signal handlers are connected and ready to use.
        """

        import user_app.api.signals
        
