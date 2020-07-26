from server.apps.main import models
from server.apps.main import tasks
from server.apps.main.logic import client_hackernews


def _mocked_get_posts_success():
    return [client_hackernews.Post(url='url', title='title')]


def test_save_hackernews_posts(db, monkeypatch):
    """This test ensures that save posts from celery task works."""
    monkeypatch.setattr(
        client_hackernews,
        'get_posts',
        _mocked_get_posts_success,
    )
    posts_count = models.HackernewsPost.objects.count()
    saved = tasks.save_hackernews_posts()
    assert saved
    assert models.HackernewsPost.objects.count() == posts_count + 1
