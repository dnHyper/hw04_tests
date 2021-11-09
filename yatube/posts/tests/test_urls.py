from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

        cls.group = Group.objects.create(
            title='Группа Test',
            slug='test_group',
            description='Описание тестовой группы'
        )

    def setUp(self):
        self.author = User.objects.create_user(username='Author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

        self.not_author = User.objects.create_user(username='not_Author')
        self.authorized_not_author_client = Client()
        self.authorized_not_author_client.force_login(self.not_author)

        self.post = Post.objects.create(
            text='Проверка',
            author=self.author,
            group=self.group
        )

        self.url_guest = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:groups'): HTTPStatus.OK,
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): HTTPStatus.OK,
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}): HTTPStatus.OK,
            reverse('posts:profile',
                    kwargs={'username': self.author.username}): HTTPStatus.OK,
            reverse('posts:feedback'): HTTPStatus.OK,
            reverse('posts:feedback_done'): HTTPStatus.OK,
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}
                    ): '/auth/login/?next=/posts/1/edit/',
            reverse('posts:post_create'): '/auth/login/?next=/create/',
                                          '/iuhhv/': HTTPStatus.NOT_FOUND
        }

    def test_url_availability_check_for_guest(self):
        """Posts: Проверка доступности страниц для гостя"""
        for reverse_name, status in self.url_guest.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.guest_client.get(reverse_name, follow=True)

                if status != HTTPStatus.OK and status != HTTPStatus.NOT_FOUND:
                    self.assertRedirects(response, status)
                else:
                    self.assertEqual(response.status_code, status)

    def test_urls_edit_check_author_for_author(self):
        """Posts: Проверка возможности автору редактировать свою запись"""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}
                    ), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_edit_check_author_on_auth_login(self):
        """Posts: Проверка защиты от редактирования записи не автором"""
        response = self.authorized_not_author_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}
                    ), follow=True)
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
