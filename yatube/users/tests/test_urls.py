from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import User


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_user = User.objects.create_user(username='User')
        cls.uid = 'test-uid'
        cls.token = 'test-token'
        cls.authorized_client = Client()

    def setUp(self):
        self.authorized_client.force_login(self.authorized_user)
        self.templates_url_names = {
            reverse('users:login'): 'users/login.html',
            reverse('users:change'
                    ): 'users/password_change_form.html',
            reverse('users:password_change_done'
                    ): 'users/password_change_done.html',
            reverse('users:password_reset_done'
                    ): 'users/password_reset_done.html',
            reverse('users:password_reset_form'
                    ): 'users/password_reset_form.html',
            reverse('users:password_reset_confirm',
                    kwargs={'uidb64': self.uid, 'token': self.token}
                    ): 'users/password_reset_confirm.html',
            reverse('users:password_reset_complet'
                    ): 'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }

    def test_auth_urls(self):
        """Users: проверка доступности страниц"""
        guest_url = {
            'login': '/auth/login/',
            'signup': '/auth/signup/',
            'reset': '/auth/reset/',
        }

        for field, expected_value in guest_url.items():
            with self.subTest(field=field):
                response = self.client.get(expected_value)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """Post: проверка доступности шаблонов."""
        for reverse_name, template in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_redirect_url(self):
        """Users: проверка перенаправлений гостя"""
        guest_url = {
            'users:change': '?next=/auth/change/',
            'users:password_change_done': '?next=/auth/password_change/done/',
        }
        for reverse_name, redirect_url in guest_url.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse(reverse_name))
                self.assertRedirects(response,
                                     reverse('users:login') + redirect_url)
