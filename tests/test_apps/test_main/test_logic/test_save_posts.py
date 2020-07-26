from server.apps.main import models
from server.apps.main.logic import client_hackernews
from server.apps.main.logic import posts


def _mocked_get_posts_success():
    return [client_hackernews.Post(url='url', title='title')]


def _mocked_get_posts_raises():
    raise client_hackernews.HackernewsParseError


def test_save_posts_success(db, monkeypatch):
    """This test ensures that save posts works."""
    monkeypatch.setattr(
        client_hackernews,
        'get_posts',
        _mocked_get_posts_success,
    )
    posts_count = models.HackernewsPost.objects.count()
    saved = posts.save_posts()
    assert saved
    assert models.HackernewsPost.objects.count() == posts_count + 1


def test_save_posts_failed(db, monkeypatch):
    """This test ensures that save posts works."""
    monkeypatch.setattr(
        client_hackernews,
        'get_posts',
        _mocked_get_posts_raises,
    )
    saved = posts.save_posts()
    assert not saved


def test_save_posts_only_unique(db, monkeypatch):
    """This test ensures that save posts only unique works."""
    monkeypatch.setattr(
        client_hackernews,
        'get_posts',
        _mocked_get_posts_success,
    )
    posts.save_posts()
    posts_count = models.HackernewsPost.objects.count()
    saved = posts.save_posts()
    assert saved
    assert models.HackernewsPost.objects.count() == posts_count
