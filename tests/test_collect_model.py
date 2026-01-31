from tests.base import BaseTestCase
from api.models import Collect


class CollectModelTestCase(BaseTestCase):
    """Тесты для модели Collect."""

    def test_collect_creation_success(self):
        """Тест успешного создания сбора."""
        collect = Collect.objects.create(
            author=self.user,
            title='Корректное название для тестового сбора',
            reason='wedding',
            description='Корректное описание для тестового сбора',
            final_price=25000,
            end_date=self.future_date
        )
        self.assertIsInstance(collect, Collect)
        self.assertEqual(
            collect.title,
            'Корректное название для тестового сбора'
        )

    def test_collect_string_representation(self):
        """Тест строкового представления сбора."""
        collect = Collect.objects.create(
            author=self.user,
            title='Тестовое название сбора',
            reason='birthday',
            description='Тестовое описание сбора',
            final_price=15000,
            end_date=self.future_date
        )
        self.assertEqual(str(collect), 'Тестовое название сбора')

    def test_collect_clean_validation_title_too_short(self):
        """Тест валидации модели при слишком коротком названии."""
        collect = Collect(
            author=self.user,
            title='Короткое',
            reason='other',
            description='Описание сбора',
            final_price=10000,
            end_date=self.future_date
        )
        with self.assertRaises(Exception):
            collect.full_clean()

    def test_collect_clean_validation_end_date_past(self):
        """Тест валидации модели при дате в прошлом."""
        collect = Collect(
            author=self.user,
            title='Корректное название для теста',
            reason='birthday',
            description='Описание сбора для теста',
            final_price=10000,
            end_date=self.past_date
        )
        with self.assertRaises(Exception):
            collect.full_clean()
