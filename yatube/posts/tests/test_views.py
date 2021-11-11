import random
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User
from yatube.settings import NUMBER_OF_POSTS


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='Author')
        cls.authorized_client = Client()

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

    def setUp(self):
        self.authorized_client.force_login(self.author)

        self.templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:groups'): 'posts/groups.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}
                    ): 'posts/group_list.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}
                    ): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}
                    ): 'posts/post_create.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse('posts:profile', kwargs={'username': self.author.username}
                    ): 'posts/profile.html',
            reverse('posts:feedback'): 'posts/feedback.html',
            reverse('posts:feedback_done'): 'posts/feedback_done.html'
        }

    def test_urls_uses_correct_template(self):
        """Post: проверка доступности шаблонов."""
        for reverse_name, template in self.templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def page_template_test_query(self, response, find):
        if find == 'page_obj':
            post = response.context.get(find).object_list[0]
        else:
            post = response.context.get('post')
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.group, self.post.group)

    def test_index_page_show_correct_context(self):
        """Post: проверка контекста шаблона index."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.page_template_test_query(response, 'page_obj')

    def test_profile_page_show_correct_context(self):
        """Post: проверка контекста шаблона profile."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': self.author.username}))

        username = response.context.get('username')
        self.page_template_test_query(response, 'page_obj')
        self.assertEqual(username.username, self.author.username)

    def test_post_page_show_correct_context(self):
        """Post: проверка контекста шаблона post_detail."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.id}))
        self.page_template_test_query(response, 'post')

    def test_group_list_page_show_correct_context(self):
        """Post: проверка контекста шаблона group_list."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}))
        group = response.context.get('group')

        self.assertEqual(group.title, self.group.title)
        self.assertEqual(group.description, self.group.description)
        self.assertEqual(group.slug, self.group.slug)
        self.page_template_test_query(response, 'page_obj')


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
        cls.add_pages = random.randint(1, NUMBER_OF_POSTS - 1)
        obj_posts = (Post(text='Проверка',
                          author=cls.author,
                          group=cls.group
                          ) for i in range(NUMBER_OF_POSTS + cls.add_pages))
        cls.post = Post.objects.bulk_create(obj_posts)
        cls.urls_paginator = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': cls.group.slug}),
            reverse('posts:profile', kwargs={'username': cls.author.username})
        }

    def test_first_page_contains_ten_records(self):
        """
        Paginator: проверка вывода постов на первую страницу.

        Количество выводимых постов получается из константы NUMBER_OF_POSTS.
        """
        for url in self.urls_paginator:
            response = self.authorized_client.get(url)
            self.assertEqual(len(response.context['page_obj']),
                             NUMBER_OF_POSTS)

    def test_second_page_contains_three_records(self):
        """Paginator: проверка вывода нескольких постов на вторую страницу."""
        for url in self.urls_paginator:
            response = self.client.get(url + '?page=2')
            self.assertEqual(len(response.context['page_obj']),
                             self.add_pages)
