import json
import logging
import typing

import typing_extensions

from django import db
from django.utils import timezone

from server.apps.main import models
from server.apps.main.logic import client_hackernews

logger = logging.getLogger(__name__)

DEFAULT_OFFSET: typing_extensions.Final = 0
DEFAULT_ORDER: typing_extensions.Final = '-created'
ALLOWED_ORDER_FIELDS: typing_extensions.Final = (
    'created', 'title', 'url', 'id',
)
DEFAULT_LIMIT: typing_extensions.Final = 5
MAX_LIMIT: typing_extensions.Final = 30
RAW_INSERT_QUERY: typing_extensions.Final = """
insert into
    main_hackernewspost (url, title, created)
select url, title, created from
    json_populate_recordset(
        NULL::main_hackernewspost,
        %s
    ) r
where not exists (
    select
        1
    from
        main_hackernewspost h
    where
        h.url = r.url and
        h.title = r.title
)
"""  # noqa: WPS323


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


def _save_only_unique_posts(posts: typing.List[client_hackernews.Post]):
    json_posts = []
    for post in reversed(posts):
        json_posts.append({
            'url': post.url,
            'title': post.title,
            'created': timezone.now().isoformat(),
        })
    with db.connection.cursor() as cursor:
        cursor.execute(
            RAW_INSERT_QUERY,
            [json.dumps(json_posts)],
        )


def save_posts() -> bool:
    """Save posts from hackernews.

    Returns True if success, False if failed.
    """
    try:
        posts = client_hackernews.get_posts()
    except (
        client_hackernews.HackernewsRequestError,
        client_hackernews.HackernewsParseError,
    ) as exc:
        error_message = 'save posts failed: {0}'.format(str(exc))
        logger.error(error_message)
        return False
    _save_only_unique_posts(posts)
    return True
