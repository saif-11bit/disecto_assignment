import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid_consultancy.settings')

app = Celery('covid_consultancy')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
