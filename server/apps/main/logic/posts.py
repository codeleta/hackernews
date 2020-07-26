import typing

import typing_extensions

from server.apps.main import models

DEFAULT_OFFSET: typing_extensions.Final = 0
DEFAULT_ORDER: typing_extensions.Final = '-created'
ALLOWED_ORDER_FIELDS: typing_extensions.Final = (
    'created', 'title', 'url', 'id',
)
DEFAULT_LIMIT: typing_extensions.Final = 5
MAX_LIMIT: typing_extensions.Final = 30


class ValidationError(Exception):
    """Raise when field value is invalid."""


def clean_limit(limit: typing.Optional[int]) -> int:
    """Validate limit.

    :raise ValidationError if value less than 0.
    :return limit or DEFAULT_LIMIT.
    """
    if limit is None:
        limit = DEFAULT_LIMIT
    limit = min(limit, MAX_LIMIT)
    if limit > 0:
        return limit
    raise ValidationError('limit must be greater than 0.')


def clean_offset(offset: typing.Optional[int]) -> int:
    """Validate offset.

    :raise ValidationError if value less than 0.
    :return offset or DEFAULT_OFFSET.
    """
    offset = offset or DEFAULT_OFFSET
    if offset >= 0:
        return offset
    raise ValidationError('offset must be greater than or equal 0.')


def clean_order(order: typing.Optional[str]) -> str:
    """Validate order.

    :raise ValidationError if value not in ALLOWED_ORDER_FIELDS.
    :return order or DEFAULT_ORDER.
    """
    order = order or DEFAULT_ORDER
    order_field = order[1:] if order.startswith('-') else order
    if order_field in ALLOWED_ORDER_FIELDS:
        return order
    raise ValidationError(
        'invalid order field "{0}". order must be one of {1}'.format(
            order_field, ALLOWED_ORDER_FIELDS,
        ),
    )


def get_posts(
    *,
    order: typing.Optional[str],
    limit: typing.Optional[int],
    offset: typing.Optional[int],
) -> typing.List[models.HackernewsPost]:
    """Get hackernews posts.

    :param ordering - name of field in HackernewsPost.
    ordering can starts with '-' — descent ordering.
    """
    limit = clean_limit(limit)
    offset = clean_offset(offset)
    order = clean_order(order)

    posts = models.HackernewsPost.objects.all()
    posts = posts.order_by(order)[offset:offset + limit]
    return list(posts)
