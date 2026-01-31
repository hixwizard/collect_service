from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from api.models import Collect
from tests.base import BaseTestCase


class CollectViewSetTestCase(BaseTestCase):
    """Тесты для ViewSet сборов."""

    def setUp(self):
        """Настройка тестовых данных для сборов."""
        super().setUp()

    def test_create_collect_success(self):
        """Тест успешного создания сбора."""
        url = reverse('collect-list')
        future_date = timezone.now() + timedelta(days=60)
        data = {
            'title': 'Новый сбор для проверки функционала',
            'reason': 'wedding',
            'description': 'Описание нового сбора для проверки',
            'final_price': 50000,
            'end_date': future_date.isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Collect.objects.filter(
            title='Новый сбор для проверки функционала',
        ).exists())

    def test_create_collect_validation_error_title_too_short(self):
        """Тест ошибки валидации при слишком коротком названии."""
        url = reverse('collect-list')
        data = {
            'title': 'Короткое',
            'reason': 'other',
            'description': 'Описание тестового сбора',
            'final_price': 10000,
            'end_date': (timezone.now() + timedelta(days=30)).isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Название сбора должно быть не менее 15 символов',
                      str(response.data))

    def test_create_collect_validation_error_end_date_past(self):
        """Тест ошибки валидации при дате в прошлом."""
        url = reverse('collect-list')
        past_date = timezone.now() - timedelta(days=1)
        data = {
            'title': 'Тестовый сбор для проверки даты',
            'reason': 'birthday',
            'description': 'Описание тестового сбора для проверки даты',
            'final_price': 10000,
            'end_date': past_date.isoformat(),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_collects_list(self):
        """Тест получения списка сборов."""
        url = reverse('collect-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_collect_detail(self):
        """Тест получения детальной информации о сборе."""
        url = reverse('collect-detail', kwargs={'pk': self.collect.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.collect.title)

    def test_get_collect_detail_not_found(self):
        """Тест получения несуществующего сбора."""
        url = reverse('collect-detail', kwargs={'pk': 1000})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
