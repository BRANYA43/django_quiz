from accounts.views import UserRegisterView, user_activate, user_profile_view

from django.test import SimpleTestCase
from django.urls import resolve, reverse


class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('accounts:register')
        self.assertIs(UserRegisterView, resolve(url).func.view_class)

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertIs(user_profile_view, resolve(url).func)

    def test_activate_user_url_resolves(self):
        url = reverse('accounts:register_activate', kwargs={'sign': 'egaugnal-looc-yrev-nohtyp'})
        self.assertIs(user_activate, resolve(url).func)
