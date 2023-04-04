from datetime import datetime, timedelta, time

from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.management import call_command
from django.utils import timezone
from django.utils.timezone import make_aware
from prettytable import PrettyTable

from .models import Result

logger = get_task_logger(__name__)


@shared_task
def simple_task():
    logger.info('>>> SIMPLE TASK <<<')


@shared_task
def send_email_report():
    call_command('send_report')


@shared_task
def send_email_reminder():
    start = make_aware(datetime.combine(timezone.now() - timedelta(7), time()))
    end = make_aware(datetime.combine(timezone.now() + timedelta(1), time()))
    results = Result.objects.filter(create_timestamp__range=(start, end), state=0).order_by('user')

    if results:
        tab_fields = ['Test', 'Start Date']
        user_results = {}
        for result in results:
            if user_results.get(result.user) is None:
                user_results[result.user] = []
            user_results[result.user].append([result.exam.title, result.create_timestamp.strftime('%Y-%m-%d %H:%M')])

        for user, results_ in user_results.items():
            tab = PrettyTable()
            tab.field_names = tab_fields
            tab.add_rows(results_)

            subject = 'You forgot to finished some exams.'
            body = f'{tab.get_string()}'
            user.email_user(subject, body)

        logger.info('>>> Results was sent. <<<')

    else:
        logger.info('>>> Nothing to send. <<<')
