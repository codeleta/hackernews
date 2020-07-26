import collections
import json

import pytest

from django import urls

TestCase = collections.namedtuple(
    'TestCase',
    'data expected_status_code expected_error_response expected_posts_count',
)


@pytest.mark.parametrize(
    'test_case',
    [
        pytest.param(
            TestCase(
                data={},
                expected_status_code=200,
                expected_error_response=None,
                expected_posts_count=5,
            ),
            id='success_without_data',
        ),
        pytest.param(
            TestCase(
                data={'order': 'title', 'limit': 3, 'offset': 5},
                expected_status_code=200,
                expected_error_response=None,
                expected_posts_count=3,
            ),
            id='success_with_data',
        ),
        pytest.param(
            TestCase(
                data={'order': '-invalid', 'limit': '0', 'offset': 'invalid'},
                expected_status_code=400,
                expected_error_response={
                    'code': 'bad_request',
                    'details': {
                        'limit': ['limit must be greater than 0.'],
                        'offset': ['Enter a whole number.'],
                        'order': [
                            'invalid order field "invalid". '
                            'order must be one of '  # noqa: WPS326
                            "('created', 'title', 'url', 'id')",  # noqa: WPS326
                        ],
                    },
                    'message': 'invalid GET data',
                },
                expected_posts_count=None,
            ),
            id='error_invalid_request_data',
        ),
    ],
)
def test_get_posts_view(
    db,
    client,
    test_case: TestCase,
):
    """This test ensures that all response cases works."""
    response = client.get(
        urls.reverse('main:get_posts'),
        data=test_case.data,
    )
    posts = json.loads(response.content)

    assert response.status_code == test_case.expected_status_code, posts

    if test_case.expected_status_code == 200:
        assert 'posts' in posts, posts
        assert len(posts['posts']) == test_case.expected_posts_count
    else:
        assert posts == test_case.expected_error_response


def test_get_posts_view_error_another_request_method(client):
    """This test ensures that allowed only GET method."""
    response = client.post(urls.reverse('main:get_posts'))
    error = json.loads(response.content)

    expected_status_code = 400
    expected_error = {
        'code': 'bad_request',
        'details': {},
        'message': 'only GET request',
    }
    assert response.status_code == expected_status_code, error
    assert error == expected_error
