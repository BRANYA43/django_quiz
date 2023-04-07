from uuid import uuid4
from django.db import models

from accounts.models import User


class Task(models.Model):
    class STATUS(models.IntegerChoices):
        NEW = 0, 'NEW'
        DONE = 1, 'DONE'

    uuid = models.UUIDField(default=uuid4, db_index=True, unique=True)
    user = models.ForeignKey(to=User, related_name='tasks', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS.choices, default=STATUS.NEW)

    class Meta:
        db_table = 'tasks'
