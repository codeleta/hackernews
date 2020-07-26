import typing

import typing_extensions

from django.db import models

MAX_TITLE_LENGTH: typing_extensions.Final = 255


@typing_extensions.final
class HackernewsPost(models.Model):
    """Hackernews post model."""

    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.URLField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        unique_together = [['title', 'url']]
        ordering = ('-created',)
        verbose_name = 'Hackernews post'
        verbose_name_plural = 'Hackernews posts'

    def __str__(self) -> str:
        """Return object as str."""
        return f'Post "{self.title}"'

    def to_dict(self) -> typing.Dict[str, typing.Union[str, int]]:
        """Return object as dict."""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'created': self.created.isoformat(timespec='seconds'),
        }
