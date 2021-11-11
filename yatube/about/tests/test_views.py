from django.test import TestCase
from django.urls import reverse


class AboutViewsTests(TestCase):
    def test_about_page_accessible_by_name(self):
        """About: проверка генерации URL about:author"""
        response = self.client.get(reverse('about:author'))
        self.assertEqual(response.status_code, 200)

    def test_tech_page_accessible_by_name(self):
        """About: проверка генерации URL about:tech"""
        response = self.client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, 200)
