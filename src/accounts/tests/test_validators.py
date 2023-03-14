from unittest import TestCase

from django.core.exceptions import ValidationError

from accounts.models import User
from accounts.validators import validate_email_exist


class TestValidators(TestCase):
    email = 'user@test.com'

    def setUp(self):
        User.objects.create(
            username='user',
            password='123qwe!@#',
            email=self.email
        )

    def test_validate_email_exist(self):
        # exist email
        self.assertIsNone(validate_email_exist(self.email))

        # not exist email
        self.assertRaises(ValidationError, validate_email_exist, self.email + '123')
