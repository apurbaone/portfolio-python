from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        # import signal handlers
        try:
            import blog.signals  # noqa: F401
        except Exception:
            pass
