"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
from __future__ import absolute_import
import os
from celery import Celery

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
from rest_api_video import settings
import logging

from video_hosting.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_api_video.settings')

app = Celery("rest_api_video")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



from django.apps import apps


@app.task
def clear_comments():
    Comment = apps.get_model("video_hosting.Comment")
    comments = Comment.objects.all()
    list_of_words = ['fuck', 'asshole', 'dumb', 'pussy', 'faggot']
    total = 0
    for comment in comments:
        for word in list_of_words:
            if word in comment.content:
                owner_id = comment.owner_id
                user_to_ban = User.objects.get(id=owner_id)
                user_to_ban.abuse_comments_counter += 1
                user_to_ban.save()
                comment.delete()
                total += 1
    logging.info(f"deleted {total}")



@app.task
def block_user_for_abuse_comments():
    User = apps.get_model("video_hosting.Comment")
    users = User.objects.filter(abuse_comments_counter__gte=10)
    total = 0
    for user in users:
        user.is_banned = True
        user.save()
        total += 1
    logging.info(f'deleted {total}')


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'video_hosting.tasks.remove_hash_tag_duplicate',
        'schedule': 10.0
    },
}