from server.apps.main.logic import post_forms


def test_posts_request_form_success():
    """This test ensures that form is valid with valid data."""
    form = post_forms.PostsRequest({
        'order': 'id',
        'limit': '5',
        'offset': '5',
    })
    assert form.is_valid()


def test_posts_request_form_invalid():
    """This test ensures that form is invalid with invalid data."""
    form = post_forms.PostsRequest({
        'order': 'invalid',
        'limit': '0',
        'offset': '-1',
    })
    assert not form.is_valid()
    assert form.errors == {
        'limit': ['limit must be greater than 0.'],
        'offset': ['offset must be greater than or equal 0.'],
        'order': [
            'invalid order field "invalid". '
            'order must be one of '  # noqa: WPS326
            "('created', 'title', 'url', 'id')",  # noqa: WPS326
        ],
    }
