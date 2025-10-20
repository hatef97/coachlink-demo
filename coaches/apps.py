from django.apps import AppConfig



class CoachesConfig(AppConfig):
    name = 'coaches'
    def ready(self):
        from . import signals 
