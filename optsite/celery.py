import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optsite.settings')

app = Celery('optsite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.update(
    task_soft_time_limit=10,
    task_time_limit=15,
)

app.control.time_limit('optsite',
                           soft=10, hard=15, reply=True)