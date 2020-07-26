import pytest

from server.apps.main.urls import app_name


def test_initial0001(migrator):
    """Tests the initial migration forward application."""
    old_state = migrator.apply_initial_migration((app_name, None))
    with pytest.raises(LookupError):
        # This model does not exist before this migration:
        old_state.apps.get_model(app_name, 'HackernewsPost')

    new_state = migrator.apply_tested_migration((app_name, '0001_initial'))
    model = new_state.apps.get_model(app_name, 'HackernewsPost')

    assert model.objects.create(title='test', url='http://example.com/title')
