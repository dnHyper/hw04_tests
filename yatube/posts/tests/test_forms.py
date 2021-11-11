from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, User, Group


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Группа Test',
            slug='test_group',
            description='Описание тестовой группы'
        )

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
        Post.objects.filter(pk=self.post.pk).update(text=form_data['text'])
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, form_data['text'])
        self.assertEqual(self.post.author, self.author)

    def test_guest_post_create(self):
        """Post: Проверка создания записи гостем"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id
        }
        response = self.client.post(
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
        Post.objects.filter(pk=self.post.pk).update(
            text=new_data['text'],
            group=new_group
        )
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, new_data['text'])
        self.assertEqual(self.post.group, new_group)
