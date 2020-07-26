from typing import Optional

import pytest

from server.apps.main import models
from server.apps.main.logic import client_hackernews
from server.apps.main.logic import posts


def _check_order_desc(
    post1: models.HackernewsPost,
    post2: models.HackernewsPost,
    attr_name: str,
):
    post1_attr = getattr(post1, attr_name)
    post2_attr = getattr(post2, attr_name)
    assert post1_attr >= post2_attr


def _check_order_asc(
    post1: models.HackernewsPost,
    post2: models.HackernewsPost,
    attr_name: str,
):
    post1_attr = getattr(post1, attr_name)
    post2_attr = getattr(post2, attr_name)
    assert post1_attr <= post2_attr, (post1_attr, post2_attr)


@pytest.mark.parametrize(
    'order',
    [
        'created',
        'title',
        'url',
        'id',
        '-created',
        '-title',
        '-url',
        '-id',
    ],
)
def test_get_posts_order(db, order: Optional[str]):
    """This test ensures that ordering works correct."""
    test_posts = posts.get_posts(order=order, limit=30, offset=0)
    if order.startswith('-'):
        order_field = order[1:]
        check_func = _check_order_desc
    else:
        order_field = order
        check_func = _check_order_asc
    for post_index in range(len(test_posts) - 1):
        check_func(
            test_posts[post_index],
            test_posts[post_index + 1],
            order_field,
        )


def test_get_posts_limit(db):
    """This test ensures that limit works correct."""
    limit = 30
    test_posts = posts.get_posts(order=None, limit=limit, offset=0)
    assert len(test_posts) == limit


@pytest.mark.parametrize(
    'offset',
    [0, 1, 5, 30],
)
def test_get_posts_offset(db, offset):
    """This test ensures that offset works correct."""
    test_posts = posts.get_posts(order='id', limit=1, offset=offset)
    assert test_posts[0].pk == offset + 1


def test_get_posts_offset_empty(db):
    """This test ensures that offset bigger than objects return nothing."""
    test_posts = posts.get_posts(order='id', limit=1, offset=50)
    assert not test_posts


def test_save_posts_success(db, monkeypatch):
    """This test ensures that save posts works."""
    def mocked_get_posts():
        return [client_hackernews.Post(url='url', title='title')]
    monkeypatch.setattr(client_hackernews, 'get_posts', mocked_get_posts)
    posts_count = models.HackernewsPost.objects.count()
    saved = posts.save_posts()
    assert saved
    assert models.HackernewsPost.objects.count() == posts_count + 1


def test_save_posts_failed(db, monkeypatch):
    """This test ensures that save posts works."""
    def mocked_get_posts():
        raise client_hackernews.HackernewsParseError
    monkeypatch.setattr(client_hackernews, 'get_posts', mocked_get_posts)
    saved = posts.save_posts()
    assert not saved
