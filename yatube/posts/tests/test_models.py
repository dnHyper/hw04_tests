from django.test import TestCase

from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Ж' * 100,
        )

    def test_title_label(self):
        """verbose_name поля text совпадает с ожидаемым."""
        verbose = self.post._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Текст сообщения')

    def test_pub_date_label(self):
        """verbose_name поля pub_date совпадает с ожидаемым."""
        verbose = self.post._meta.get_field('pub_date').verbose_name
        self.assertEqual(verbose, 'Дата публикации')

    def test_author_label(self):
        """verbose_name поля author совпадает с ожидаемым."""
        verbose = self.post._meta.get_field('author').verbose_name
        self.assertEqual(verbose, 'Автор')

    def test_group_label(self):
        """verbose_name поля group совпадает с ожидаемым."""
        verbose = self.post._meta.get_field('group').verbose_name
        self.assertEqual(verbose, 'Группа')

    def test_post_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        expected_object_name = self.post.text[:25]
        self.assertEqual(expected_object_name, str(expected_object_name))

    def test_group_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        expected_object_name = self.group.title
        self.assertEqual(expected_object_name, str(expected_object_name))
