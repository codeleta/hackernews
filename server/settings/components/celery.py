from celery import schedules

from server.settings.vars import common_vars

CELERY_BEAT_SCHEDULE = {
    'save-hackernews-posts': {
        'task': 'server.apps.main.tasks.save_hackernews_posts',
        'schedule': schedules.crontab(),
    },
}

CELERY_IGNORE_RESULT = True

CELERY_BROKER_URL = 'redis://{0}:{1}/0'.format(
    common_vars.config('REDIS_HOST'),
    common_vars.config('REDIS_PORT'),
)
