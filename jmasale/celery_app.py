import os

from celery import Celery

# Ensure Celery workers load the correct Django settings.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jmasale.settings")

app = Celery("jmasale")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

