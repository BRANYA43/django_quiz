from accounts.forms import UserRegisterForm, UserUpdateForm
from accounts.models import User

from django.core.signing import Signer
from django.test import Client, TestCase
from django.urls import reverse


class TestUserRegisterView(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user_1',
            'password1': '123qwe!@#',
            'password2': '123qwe!@#',
            'email': 'user_1@test.com',
        }
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.register_done_url = reverse('accounts:register_done')

    def test_contain_template(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'accounts/user_register.html')

    def test_contain_form(self):
        response = self.client.get(self.register_url)
        form = response.context.get('form')
        self.assertIsInstance(form, UserRegisterForm)

    def test_success_redirect(self):
        response = self.client.post(self.register_url, self.data)
        self.assertRedirects(response, self.register_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.register_done_url)

    def test_not_success_redirect(self):
        self.data['password1'] = '123qwe!@'
        response = self.client.post(self.register_url, self.data)
        self.assertNotEqual(302, response.status_code)

    def test_registration_valid(self):
        self.client.post(self.register_url, self.data)

        user = User.objects.first()

        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['email'], user.email)
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_register_invalid(self):
        self.data['password1'] = '123qwe!@'

        response = self.client.post(self.register_url, self.data)
        form = response.context['form']
        user = User.objects.filter(username=self.data['username'])

        self.assertFalse(form.is_valid())
        self.assertEqual(0, len(user))


class TestUserLoginView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('accounts:login')

    def test_contain_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/user_login.html')


class TestUserLogoutView(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse('accounts:logout')

    def test_contain_template(self):
        User.objects.create_user(username='user', password='123qwe!@#')
        self.client.login(username='user', password='123qwe!@#')
        response = self.client.post(self.url)
        self.assertTemplateUsed(response, 'accounts/user_logout.html')
