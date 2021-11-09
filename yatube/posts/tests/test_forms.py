from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, User, Group
from posts.forms import PostForm


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

        cls.group = Group.objects.create(
            title='Группа Test',
            slug='test_group',
            description='Описание тестовой группы'
        )
        cls.form = PostForm()

    def setUp(self):
        self.author = User.objects.create_user(username='Author')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)
        self.post = Post.objects.create(
            text='Проверка',
            author=self.author,
            group=self.group
        )

    def test_create_post(self):
        """Post: проверка создания записи через форму"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
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
                text='Тестовый текст',
                author=self.author,
            ).exists()
        )

    def test_guest_post_create(self):
        """Post: Проверка создания записи гостем"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        response = self.guest_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'users:login') + '?next=/create/'
        )
        self.assertEqual(Post.objects.count(), post_count)

    def test_edit_post_other_user(self):
        """Post: Проверка редактирования другим пользователем чужой записи"""
        self.editor = User.objects.create_user(username='User')
        self.editor_client = Client()
        self.editor_client.force_login(self.editor)
        new_data = {
            'text': 'Отредактированный текст',
        }
        response = self.editor_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=new_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )

    def test_edit_post(self):
        """Post: Проверка редактирования записи"""
        new_group = Group.objects.create(
            title='Группа Test',
            slug='test_group_2',
            description='Описание тестовой группы'
        )
        new_data = {
            'text': 'Отредактированный текст',
            'group': new_group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=new_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Отредактированный текст',
                group=new_group.id
            ).exists()
        )
