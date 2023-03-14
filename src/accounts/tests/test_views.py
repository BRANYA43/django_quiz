from accounts.forms import UserReactivationForm, UserRegisterForm, UserUpdateForm
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
        self.registration_url = reverse('accounts:register')
        self.registration_done_url = reverse('accounts:register_done')

    def test_contain_template(self):
        response = self.client.get(self.registration_url)
        self.assertTemplateUsed(response, 'accounts/user_register.html')

    def test_contain_form(self):
        response = self.client.get(self.registration_url)
        form = response.context.get('form')
        self.assertIsInstance(form, UserRegisterForm)

    def test_success_redirect(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.registration_done_url)

    def test_not_success_redirect(self):
        self.data['password1'] = '123qwe!@'
        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(302, response.status_code)

    def test_registration_valid(self):
        self.client.post(self.registration_url, self.data)

        user = User.objects.first()

        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['email'], user.email)
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_register_invalid(self):
        self.data['password1'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
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
        login_data = {
            'username': 'user',
            'password': '123qwe!@#',
        }
        User.objects.create_user(**login_data)
        self.client.login(**login_data)
        response = self.client.post(self.url)
        self.assertTemplateUsed(response, 'accounts/user_logout.html')


class TestUserProfileUpdateView(TestCase):
    def setUp(self) -> None:
        self.login_data = {
            'username': 'user',
            'password': '123qwe!@#',
        }
        self.required_data = {
            'username': self.login_data['username'],
            'email': 'user@test.com',
        }
        self.not_required_data = {
            'firs_name': 'user_first_name',
            'last_name': 'user_last_name',
            # TODO 'birthday': '08.03.2023',
            'city': 'Kharkov',
        }
        self.full_data = {**self.required_data, **self.not_required_data}
        self.client = Client()
        self.user = User.objects.create_user(**self.login_data)
        self.client.login(**self.login_data)
        self.profile_update_url = reverse('accounts:profile_update')
        self.profile_url = reverse('accounts:profile')

    def test_contain_template(self):
        response = self.client.get(self.profile_update_url)
        self.assertTemplateUsed(response, 'accounts/user_profile_update.html')

    def test_contain_form(self):
        response = self.client.get(self.profile_update_url)
        form = response.context.get('form')
        self.assertIsInstance(form, UserUpdateForm)

    def test_success_redirect_required_data(self):
        response = self.client.post(self.profile_update_url, self.required_data)
        self.assertRedirects(response, self.profile_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.profile_url)

    def test_success_redirect_required_full_data(self):
        response = self.client.post(self.profile_update_url, self.full_data)
        self.assertRedirects(response, self.profile_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.profile_url)

    def test_not_success_redirect(self):
        self.required_data = {}
        response = self.client.post(self.profile_update_url, self.required_data)
        self.assertNotEqual(302, response.status_code)

        self.not_required_data.update(self.required_data)
        response = self.client.post(self.profile_update_url, self.not_required_data)
        self.assertNotEqual(302, response.status_code)


class TestUserReactivationView(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user',
            'password': '123qwe!@#',
            'email': 'user@test.com',
        }
        User.objects.create_user(**self.data)
        self.client = Client()
        self.reactivation_url = reverse('accounts:reactivation')
        self.reactivation_done_url = reverse('accounts:reactivation_done')

    def test_contain_template(self):
        response = self.client.get(self.reactivation_url)
        self.assertTemplateUsed(response, 'accounts/user_reactivation.html')

    def test_contain_form(self):
        response = self.client.get(self.reactivation_url)
        form = response.context.get('form')
        self.assertIsInstance(form, UserReactivationForm)

    def test_success_redirect(self):
        response = self.client.post(self.reactivation_url, {'email': self.data['email']})
        self.assertRedirects(response, self.reactivation_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.reactivation_done_url)

    def test_not_success_redirect(self):
        self.data['email'] = 'not_exist_user@test.com'
        response = self.client.post(self.reactivation_url, {'email': self.data['email']})
        self.assertNotEqual(302, response.status_code)


class TestUserActivate(TestCase):
    def setUp(self) -> None:
        self.data = {
            'username': 'user_1',
            'password1': '123qwe!@#',
            'password2': '123qwe!@#',
            'email': 'user_1@test.com',
        }
        self.client = Client()
        self.registration_url = reverse('accounts:register')
        self.registration_done_url = reverse('accounts:register_done')

    def test_activation_url(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(self.data['username'], user.username)

        signer = Signer()
        response = self.client.get(
            'http://localhost' + reverse('accounts:register_activate', kwargs={'sign': signer.sign(user.username)})
        )
        self.assertEqual(200, response.status_code)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_activated)
