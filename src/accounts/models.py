import os.path

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def save_avatar(instance, filename):
    filename = f'profile/{instance.username}_logo'
    if os.path.exists(settings.MEDIA_ROOT / filename):
        os.remove(settings.MEDIA_ROOT / filename)
    return filename


class User(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True)
    avatar = models.ImageField(upload_to=save_avatar, default='profile/default.png')
    birthday = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = 'users'

    def __str__(self):
        return self.username
