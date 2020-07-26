import pytest
import requests_mock

from server.apps.main.logic import client_hackernews


def test_get_posts_success():
    """This test ensures that get posts works."""
    post_url = 'http://example.com'
    post_title = 'Title'
    with requests_mock.Mocker() as mocked_requests:
        mocked_requests.get(
            client_hackernews.HACKERNEWS_HOST,
            text=f'<a href="{post_url}" class="storylink">{post_title}</a>',
        )
        posts = client_hackernews.get_posts()
    expected_posts = [client_hackernews.Post(url=post_url, title=post_title)]
    assert posts == expected_posts


def test_get_posts_requests_error():
    """This test ensures that requests error raises HackernewsRequestError."""
    with requests_mock.Mocker() as mocked_requests:
        mocked_requests.get(
            client_hackernews.HACKERNEWS_HOST,
            status_code=500,
            text='internal error',
        )
        with pytest.raises(client_hackernews.HackernewsRequestError):
            client_hackernews.get_posts()


def test_get_posts_not_found():
    """This test ensures that parser error raises HackernewsParseError."""
    with requests_mock.Mocker() as mocked_requests:
        mocked_requests.get(
            client_hackernews.HACKERNEWS_HOST,
            text='No posts',
        )
        with pytest.raises(client_hackernews.HackernewsParseError):
            client_hackernews.get_posts()
