import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

# Create the Celery application
app = Celery('crm')

# Load Celery config from Django settings with `CELERY_` namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')

app = Celery('crm')

# Load settings from Django config
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in crm/tasks.py
app.autodiscover_tasks()
