from django.apps import AppConfig
from django.dispatch import Signal, receiver

from accounts.utils import send_activation_notification


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'


user_register = Signal()


@receiver(user_register)
def user_register_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
