from server.apps.main import models


def test_hackernews_post_model_create(db):
    """This test ensures that HackernewsPost create works."""
    title = 'test title'
    instance = models.HackernewsPost.objects.create(
        title=title,
        url=f'http://example.com/{title}',
    )
    assert str(instance) == f'Post "{title}"'


def test_hackernews_post_model_to_dict(db):
    """This test ensures that HackernewsPost.to_dict works."""
    instance = models.HackernewsPost.objects.all()[0]
    expected_instance_dict = {
        'id': instance.id,
        'url': instance.url,
        'title': instance.title,
        'created': instance.created.isoformat(timespec='seconds'),
    }

    assert instance.to_dict() == expected_instance_dict
