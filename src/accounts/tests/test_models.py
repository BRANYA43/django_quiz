from accounts.models import User, save_avatar

from django.db.models import BooleanField, CharField, DateField, ImageField
from django.test import TestCase


class TestModel(TestCase):
    username = None

    @classmethod
    def setUpTestData(cls):
        cls.username = 'user_1'

        User.objects.create(
            username=cls.username,
            password='123qwe!@#',
            email='user_1@test.com'
        )

    def setUp(self) -> None:
        self.user = User.objects.get(username=self.username)

    def test_avatar_field(self):
        field = self.user._meta.get_field('avatar')
        self.assertIsInstance(field, ImageField)
        self.assertIs(save_avatar, field.upload_to)
        self.assertEqual('profile/default.png', field.default)

    def test_is_activate_field(self):
        field = self.user._meta.get_field('is_activated')
        self.assertIsInstance(field, BooleanField)
        self.assertTrue(field.default)
        self.assertTrue(field.db_index)

    def test_city_field(self):
        field = self.user._meta.get_field('birthday')
        self.assertIsInstance(field, DateField)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_birthday_field(self):
        field = self.user._meta.get_field('city')
        self.assertIsInstance(field, CharField)
        self.assertEqual(50, field.max_length)
        self.assertTrue(field.null)
        self.assertTrue(field.blank)

    def test_save_avatar(self):
        filename = save_avatar(self.user, '')
        self.assertEqual(f'profile/{self.user.username}_logo', filename)

    def test_convert_user_to_str(self):
        self.assertEqual(str(self.user), self.username)
