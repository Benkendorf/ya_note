from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteList(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.NOTES_QUANTITY = 5
        cls.author = User.objects.create(username='Лев Толстой')
        cls.other_author = User.objects.create(username='Антон Чехов')
        all_notes = [
            Note(
                title=f'Заметка {index}',
                text='Просто текст заметки.',
                slug=f'slug-{index}',
                author=cls.author
            )
            for index in range(cls.NOTES_QUANTITY)
        ]

        other_note = Note(
            title='Заметка',
            text='Просто текст заметки.',
            slug='slug-other',
            author=cls.other_author
        )

        all_notes.append(other_note)

        Note.objects.bulk_create(all_notes)

    def test_notes_count_by_author(self):
        # Загружаем главную страницу.
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        # Определяем количество записей в списке.
        notes_count = object_list.count()
        # Проверяем, что на странице именно 10 новостей.
        self.assertEqual(notes_count, TestNoteList.NOTES_QUANTITY)
