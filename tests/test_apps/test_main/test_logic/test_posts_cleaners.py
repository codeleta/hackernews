from typing import Optional

import pytest

from server.apps.main.logic import posts


@pytest.mark.parametrize(('limit', 'expected_limit'), [
    (1, 1),
    (15, 15),
    (30, 30),
    (50, 30),
    (None, 5),
])
def test_clean_limit_success(limit: Optional[int], expected_limit: int):
    """This test ensures that clean_limit works correct."""
    assert posts.clean_limit(limit) == expected_limit


@pytest.mark.parametrize(
    'limit',
    [-50, -1, 0],
)
def test_clean_limit_raise(limit: int):
    """This test ensures that clean_limit raises correct."""
    with pytest.raises(posts.ValidationError):
        assert posts.clean_limit(limit)


@pytest.mark.parametrize(('offset', 'expected_offset'), [
    (0, 0),
    (1, 1),
    (15, 15),
    (30, 30),
    (50, 50),
    (None, 0),
])
def test_clean_offset_success(offset: Optional[int], expected_offset: int):
    """This test ensures that clean_offset works correct."""
    assert posts.clean_offset(offset) == expected_offset


@pytest.mark.parametrize(
    'offset',
    [-50, -1],
)
def test_clean_offset_raise(offset: int):
    """This test ensures that clean_offset raises correct."""
    with pytest.raises(posts.ValidationError):
        assert posts.clean_offset(offset)


@pytest.mark.parametrize(('order', 'expected_order'), [
    ('created', 'created'),
    ('title', 'title'),
    ('url', 'url'),
    ('id', 'id'),
    ('-created', '-created'),
    ('-title', '-title'),
    ('-url', '-url'),
    ('-id', '-id'),
])
def test_clean_order_success(order: Optional[str], expected_order: str):
    """This test ensures that clean_order works correct."""
    assert posts.clean_order(order) == expected_order


@pytest.mark.parametrize(
    'order',
    ['invalid', '-invalid', '1', 'limit', 'objects'],
)
def test_clean_order_raise(order: str):
    """This test ensures that clean_order raises correct."""
    with pytest.raises(posts.ValidationError):
        assert posts.clean_order(order)
