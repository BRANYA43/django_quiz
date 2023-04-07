import time

from celery import shared_task
from celery.utils.log import get_task_logger

from accounts.models import User
from long_task.models import Task

logger = get_task_logger(__name__)


@shared_task
def create_task(task_type):
    time.sleep(int(task_type) * 5)
    return True


@shared_task
def user_task(pk):
    user = User.objects.get(pk=pk)
    task = Task.objects.create(user=user)
    logger.info(f'Start task {task.uuid} {task.user} {task.status}')
    time.sleep(30)
    task.user.email_user(subject='User task', message='Your user task DONE')
    task.status = task.STATUS.DONE
    task.save()
    logger.info(f'Finish task {task.uuid} {task.user} {task.status}')
    return True
