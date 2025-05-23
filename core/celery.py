# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
#
# app = Celery('core')
#
# # Configure Celery using settings from Django settings.py.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load tasks from all registered Django app configs.
# app.autodiscover_tasks()
#
#
# app.conf.update(
#     broker_connection_retry_on_startup=True,
#     broker_connection_max_retries=10,
#     broker_connection_retry=True,
#     broker_connection_retry_delay=1,
#     result_expires=3600,
#     task_track_started=True,
#     task_time_limit=30 * 60,  # 30 minutes
#     worker_prefetch_multiplier=1,
# )
