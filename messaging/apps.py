from django.apps import AppConfig



class MessagingConfig(AppConfig):
    name = "messaging"
    def ready(self):
        from . import signals  
