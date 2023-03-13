from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def validate_email_exist(value):
    model = get_user_model()
    if not model.objects.filter(email=value):
        raise ValidationError("This email is not associated with any user.")
