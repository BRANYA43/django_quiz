from accounts.forms import UserReactivationForm, UserRegisterForm, UserUpdateForm
from accounts.models import User
from accounts.validators import validate_email_exist

from django.contrib.auth.password_validation import password_validators_help_text_html
from django.forms import CharField, DateField, DateInput, EmailField, FileInput, ImageField, PasswordInput
from django.test import TestCase


class TestUserRegisterForm(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'password1': '123qwe!@#',
            'password2': '123qwe!@#',
            'email': 'user_1@test.com',
        }
        self.form = UserRegisterForm

    def test_email_field(self):
        form = self.form(self.data)
        field = form.fields['email']
        self.assertIsInstance(field, EmailField)
        self.assertEqual('email', field.label)

    def test_password1_field(self):
        form = self.form(self.data)
        field = form.fields['password1']
        self.assertIsInstance(field, CharField)
        self.assertEqual('password', field.label)
        self.assertIsInstance(field.widget, PasswordInput)
        self.assertEqual(password_validators_help_text_html, field.help_text)

    def test_password2_field(self):
        form = self.form(self.data)
        field = form.fields['password2']
        self.assertIsInstance(field, CharField)
        self.assertEqual('confirm password', field.label)
        self.assertIsInstance(field.widget, PasswordInput)
        self.assertEqual('please repeat password', field.help_text)

    def test_form_valid_data(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(4, len(form.errors))

    def test_clean_password(self):
        form = self.form(self.data)
        form.is_valid()
        self.assertEqual(self.data['password1'], form.clean_password())

    def test_clean_correct_password(self):
        form = self.form(self.data)
        form.is_valid()
        self.assertIsNone(form.clean())

    def test_clean_incorrect_password(self):
        # Not equal password and confirm password
        self.data['password1'] = '123qwe!@#'
        self.data['password2'] = '!@#qwe123'
        form = self.form(self.data)
        form.is_valid()
        # self.assertRaises(ValidationError, form.clean)

    def test_save(self):
        form = self.form(self.data)
        form.is_valid()
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(self.data['email'], user.email)
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)


class TestUserUpdateForm(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user',
            'email': 'user@test.com',
        }
        self.not_required_data = {
            'firs_name': 'user_first_name',
            'last_name': 'user_last_name',
            # TODO 'birthday': '08.03.2023',
            'city': 'Kharkov',
        }
        self.form = UserUpdateForm

    def test_avatar_field(self):
        form = self.form(self.data)
        field = form.fields['avatar']
        self.assertIsInstance(field, ImageField)
        self.assertFalse(field.required)
        self.assertIsInstance(field.widget, FileInput)

    def test_birthday_field(self):
        form = self.form(self.data)
        field = form.fields['birthday']
        self.assertIsInstance(field, DateField)
        self.assertFalse(field.required)
        self.assertIsInstance(field.widget, DateInput)

    def test_email_field(self):
        form = self.form(self.data)
        field = form.fields['email']
        self.assertIsInstance(field, EmailField)
        self.assertTrue(field.required)

    def test_form_valid_data(self):
        # required data
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

        # full data
        self.data.update(self.not_required_data)
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # no data
        form = self.form(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))

        # not required data
        form = self.form(data=self.not_required_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(2, len(form.errors))


class TestReactivationForm(TestCase):
    def setUp(self) -> None:
        self.data = {
            'email': 'user@test.com',
        }

        User.objects.create(
            username='user',
            password='123qwe!@#',
            email=self.data['email']
        )

        self.form = UserReactivationForm

    def test_email_field(self):
        form = self.form(data=self.data)
        field = form.fields['email']
        self.assertIsInstance(field, EmailField)
        self.assertTrue(field.required)
        self.assertIn(validate_email_exist, field.validators)

    def test_valid_email(self):
        form = self.form(data=self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = self.form(data={'email': '1test@te.cm'})
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))

    def test_clear_email_of_exist_user(self):
        form = self.form(data=self.data)
        form.is_valid()
        self.assertEqual(self.data['email'], form.clean_email())

    def test_clear_email_of_not_exist_user(self):
        form = self.form(data={'email': 'not_exist_user@test.com'})
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors))
