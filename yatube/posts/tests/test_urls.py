from django.test import TestCase, Client

from posts.models import Post, Group, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.author = User.objects.create_user(username='Author')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.not_author = User.objects.create_user(username='not_Author')
        cls.authorized_not_author_client = Client()
        cls.authorized_not_author_client.force_login(cls.not_author)
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

    def test_home_url_exists_at_desired_location(self):
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_posts_url_exists_at_desired_location(self):
        """Страница /posts/1/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_redirect_anonymous_on_auth_login(self):
        """Страница /create/ перенаправит анонимного пользователя на страницу
        логина.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    def test_urls_redirect_anonymous_on_auth_login(self):
        """Страница /posts/1/edit/ перенаправит анонимного пользователя
        на страницу логина. Она доступна только автору.
        """
        response = self.guest_client.get('/posts/1/edit/', follow=True)
        self.assertRedirects(
            response, ('/auth/login/?next=/posts/1/edit/'))

    def test_urls_edit_check_author_on_auth_login(self):
        """Страница /posts/1/edit/ доступна только автору."""
        response = self.authorized_client.get('/posts/1/edit/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_urls_edit_check_author_on_auth_login(self):
        """Страница /posts/1/edit/ перенаправит не-автора на /posts/1/"""
        response = self.authorized_not_author_client.get('/posts/1/edit/',
                                                         follow=True)
        self.assertRedirects(
            response, ('/posts/1/'))

    def test_urls_404_check(self):
        """Отсутствующая страница выдаёт ошибку 404"""
        response = self.guest_client.get('/iuhhv/', follow=True)
        self.assertEqual(response.status_code, 404)
