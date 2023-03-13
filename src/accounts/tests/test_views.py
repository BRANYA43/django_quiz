from accounts.models import User

from django.core.signing import Signer
from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
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

    def test_registration_valid(self):
        response = self.client.post(self.registration_url, self.data)

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)
        self.assertEqual(self.registration_done_url, response.url)

        user = User.objects.first()
        self.assertEqual(self.data['username'], user.username)
        self.assertEqual(self.data['email'], user.email)
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_registration_invalid(self):
        self.data['password2'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(302, response.status_code)
        self.assertFalse(response.context['form'].is_valid())
        user = User.objects.filter(username=self.data['username'])
        self.assertEqual(0, len(user))

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
