import dataclasses
import logging
import typing

import bs4
import requests
import typing_extensions
from requests import adapters
from urllib3.util import retry

logger = logging.getLogger(__name__)

HACKERNEWS_HOST: typing_extensions.Final = 'https://news.ycombinator.com/'


@dataclasses.dataclass
class Post(object):
    """Post from hackernews site."""

    url: str
    title: str


class HackernewsRequestError(Exception):
    """Raises when requests.get failed."""


class HackernewsParseError(Exception):
    """Raises when posts not found."""


def _requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
) -> requests.Session:
    session = session or requests.Session()
    retry_policy = retry.Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = adapters.HTTPAdapter(max_retries=retry_policy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def _get_index_page_text() -> str:
    hackernews_index_page = _requests_retry_session().get(HACKERNEWS_HOST)
    try:
        hackernews_index_page.raise_for_status()
    except requests.HTTPError as exc:
        error_message = 'Request to {0} failed with status {1}: {2}'.format(
            HACKERNEWS_HOST,
            hackernews_index_page.status_code,
            str(exc),
        )
        logger.error(error_message)
        raise HackernewsRequestError(str(exc))
    return hackernews_index_page.text


def _parse_posts(page_html: str) -> typing.List[Post]:
    parsed_html = bs4.BeautifulSoup(page_html, 'html.parser')
    posts: typing.List[Post] = []
    post_links = parsed_html.findAll('a', {'class': 'storylink'})
    if not post_links:
        error_message = 'posts not found'
        logger.error(error_message)
        raise HackernewsParseError(error_message)
    for post_link in post_links:
        posts.append(
            Post(
                url=post_link.get('href'),
                title=post_link.text,
            ),
        )
    return posts


def get_posts() -> typing.List[Post]:
    """Get posts from hackernews site."""
    return _parse_posts(_get_index_page_text())
