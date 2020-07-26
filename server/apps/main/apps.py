from django import apps


class MainConfig(apps.AppConfig):
    """Main config for django app."""

    name = 'server.apps.main'
    label = 'main'
    verbose_name = 'Main hackernews posts app'
