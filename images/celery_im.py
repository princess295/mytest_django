import os
from celery import Celery
from django.conf import settings
from .tasks import resize_image
import images.tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'images.settings')

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0', include=['tasks'])
app.config_from_object('django.conf:settings')



# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
