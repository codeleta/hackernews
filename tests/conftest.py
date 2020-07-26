"""This module is used to provide config, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""
import pathlib

import pytest

from django.core.management import call_command


@pytest.fixture(autouse=True)
def _media_root(settings, tmpdir_factory):
    """Forces django to save media files into temp folder."""
    settings.MEDIA_ROOT = tmpdir_factory.mktemp('media', numbered=True)


@pytest.fixture(autouse=True)
def _password_hashers(settings):
    """Forces django to use fast password hashers for tests."""
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]


@pytest.fixture(autouse=True)
def _auth_backends(settings):
    """Deactivates security backend from Axes app."""
    settings.AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
    )


@pytest.fixture(autouse=True)
def _templates_debug(settings):
    """Activates TEMPLATE debug mode for coverage."""
    for template in settings.TEMPLATES:
        template['OPTIONS']['debug'] = True


@pytest.fixture(autouse=True)
def _django_db_setup(django_db_blocker):
    """Load test data."""
    path_to_dump = pathlib.PurePath(__file__).parent
    path_to_dump = path_to_dump.joinpath('dumps', 'initial_data.json')
    with django_db_blocker.unblock():
        call_command('loaddata', path_to_dump)
