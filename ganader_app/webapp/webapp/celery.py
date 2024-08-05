from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

app = Celery("webapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(
    worker_concurrency=1,
)
app.conf.task_routes = {'cattle_countings.tasks.process_video': {'queue': 'queue1'}}
app.autodiscover_tasks()