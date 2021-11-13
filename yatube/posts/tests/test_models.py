from django.test import TestCase

from posts.models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

        cls.post = Post.objects.create(
            author=cls.user,
            text='Ж' * 100,
        )

    def test_posts_verbose_name_label(self):
        """Posts: тестирование у модели Post verbose_name всех полей."""
        verbose = self.post._meta
        field_verboses = {
            'text': 'Текст сообщения',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for field, value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(verbose.get_field(field).verbose_name, value)

    def test_post_have_correct_object_names(self):
        """Posts: Проверяем, что у модели Post корректно работает __str__."""
        expected_object_name = self.post.text[:25]
        self.assertEqual(expected_object_name, str(self.post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )

    def test_title_label(self):
        """Posts: тестирование у модели Group verbose_name всех полей."""
        verbose = self.group._meta
        field_verboses = {
            'title': 'Имя группы',
            'slug': 'Адрес для ЧПУ',
            'description': 'Описание группы',
        }
        for field, value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(verbose.get_field(field).verbose_name, value)

    def test_group_have_correct_object_names(self):
        """Posts: Проверяем, что у модели Group корректно работает __str__."""
        expected_object_name = self.group.title
        self.assertEqual(expected_object_name, str(self.group))
