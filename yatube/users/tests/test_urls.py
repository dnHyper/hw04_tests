from django.test import TestCase, Client


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_auth_urls(self):
        url = {
            'login': '/auth/login/',
            'signup': '/auth/signup/',
            'reset': '/auth/reset/',
        }

        for field, expected_value in url.items():
            with self.subTest(field=field):
                response = self.guest_client.get(expected_value)
                self.assertEqual(response.status_code, 200)
