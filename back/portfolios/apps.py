from django.apps import AppConfig


class PortfoliosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolios'

    def ready(self):
        import portfolios.signals  # 시그널 파일을 임포트하여 연결
