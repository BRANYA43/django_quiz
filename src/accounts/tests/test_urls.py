from accounts.views import UserLoginView, UserLogoutView, UserProfileUpdateView, UserReactivationView, UserRegisterView, \
    user_activate, user_profile_view

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from django.views.generic import TemplateView


class TestUrls(SimpleTestCase):

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertIs(user_profile_view, resolve(url).func)

    def test_register_url_resolve(self):
        url = reverse('accounts:register')
        self.assertIs(UserRegisterView, resolve(url).func.view_class)

    def test_register_activated_url_resolve(self):
        url = reverse('accounts:register_activate', kwargs={'sign': 'egaugnal-looc-yrev-nohtyp'})
        self.assertIs(user_activate, resolve(url).func)

    def test_register_done_url_resolve(self):
        url = reverse('accounts:register_done')
        self.assertIs(TemplateView, resolve(url).func.view_class)

    def test_reactivation_url_resolve(self):
        url = reverse('accounts:reactivation')
        self.assertIs(UserReactivationView, resolve(url).func.view_class)

    def test_reactivation_done_url_resolve(self):
        url = reverse('accounts:reactivation_done')
        self.assertIs(TemplateView, resolve(url).func.view_class)

    def test_login_url_resolve(self):
        url = reverse('accounts:login')
        self.assertIs(UserLoginView, resolve(url).func.view_class)

    def test_logout_url_resolve(self):
        url = reverse('accounts:logout')
        self.assertIs(UserLogoutView, resolve(url).func.view_class)

    def test_profile_url_resolve(self):
        url = reverse('accounts:profile')
        self.assertIs(user_profile_view, resolve(url).func)

    def test_profile_update_url_resolve(self):
        url = reverse('accounts:profile_update')
        self.assertIs(UserProfileUpdateView, resolve(url).func.view_class)
