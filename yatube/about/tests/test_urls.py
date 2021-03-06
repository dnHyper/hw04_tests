from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class AboutURLTests(TestCase):
    def setUp(self):
        self.templates_url_names = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html'
        }

    def test_urls_uses_correct_template(self):
        """About: проверка доступности шаблонов."""
        for reverse_name, template in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        """About: проверка доступности страниц."""
        for reverse_name in self.templates_url_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)
