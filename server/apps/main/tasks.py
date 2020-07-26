from server import celery
from server.apps.main.logic import posts


@celery.app.task()
def save_hackernews_posts():
    """Celery task save posts from hackernews."""
    return posts.save_posts()
