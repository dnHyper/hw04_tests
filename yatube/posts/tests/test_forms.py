from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, User, Group
from posts.forms import PostForm


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.author = User.objects.create_user(username='Author')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.group = Group.objects.create(
            title='Группа Test',
            slug='test_group',
            description='Описание тестовой группы'
        )
        cls.post = Post.objects.create(
            text='Проверка',
            author=cls.author
        )
        cls.form = PostForm()

    def test_create_post(self):
        """Проверка создания записи через форму"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'author': self.authorized_client
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': self.author.username})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст'
            ).exists()
        )

    def test_edit_post(self):
        """Проверка редактирования записи"""
        form_data = {
            'text': 'Отредактированный текст',
            'author': self.author,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
            ).exists()
        )
