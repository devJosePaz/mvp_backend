from django.apps import AppConfig

class AppIaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_ia'
    
    def ready(self):
        import sys
        # Não carrega IA durante comandos de migração
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            try:
                from app_ia.algoritmo_ia.services import IARecommendationService
                IARecommendationService()
            except ImportError as e:
                print(f"⚠️ IA não carregada (erro não crítico): {str(e)}")