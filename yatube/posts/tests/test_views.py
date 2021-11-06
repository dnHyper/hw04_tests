from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            author=cls.author,
            group=cls.group
        )
        cls.templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:groups'): 'posts/groups.html',
            reverse('posts:group_list', kwargs={'slug': cls.group.slug}
                    ): 'posts/group_list.html',
            reverse('posts:post_detail', kwargs={'post_id': cls.post.id}
                    ): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': cls.post.id}
                    ): 'posts/post_create.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:profile', kwargs={'username': cls.author.username}
                    ): 'posts/profile.html',
            reverse('posts:feedback'): 'posts/feedback.html',
            reverse('posts:feedback_done'): 'posts/feedback_done.html'
        }

    def test_urls_uses_correct_template(self):
        """Проверка доступности шаблонов."""
        for reverse_name, template in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        post = response.context.get('page_obj').object_list[0]
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group, self.post.group)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.author.username}))
        post = response.context.get('page_obj').object_list[0]
        username = response.context.get('username')
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group, self.post.group)
        self.assertEqual(username.username, self.author.username)

    def test_post_page_show_correct_context(self):
        """Шаблон post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        post = response.context.get('post')
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group, self.group)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}))
        group = response.context.get('group')
        post = response.context.get('page_obj').object_list[0]
        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.description, self.group.description)
        self.assertEqual(group.slug, self.group.slug)
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group, self.post.group)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Author')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)

        cls.group = Group.objects.create(
            title='Группа Test',
            slug='test_group',
            description='Описание тестовой группы'
        )

        for i in range(13):
            cls.post = Post.objects.create(
                text=f'Проверка-{i}',
                author=cls.author,
                group=cls.group
            )

        cls.urls_paginator = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': cls.group.slug}),
            reverse('posts:profile', kwargs={'username': cls.author.username})
        }

    def test_first_page_contains_ten_records(self):
        """Проверка Paginator: вывод 10 постов на первую страницую."""
        for url in self.urls_paginator:
            response = self.client.get(url)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """Проверка Paginator: вывод 3 постов на вторую страницую."""
        for url in self.urls_paginator:
            response = self.client.get(url + '?page=2')
            self.assertEqual(len(response.context['page_obj']), 3)
