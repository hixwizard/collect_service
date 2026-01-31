from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from api.models import Collect

User = get_user_model()


class BaseTestCase(TestCase):
    """Базовый тестовый класс."""

    @classmethod
    def setUpTestData(cls):
        """Создание тестовых данных."""
        super().setUpTestData()
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        cls.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        cls.future_date = timezone.now() + timedelta(days=30)
        cls.collect = Collect.objects.create(
            author=cls.user,
            title='Тестовый сбор для друзей и семьи',
            reason='birthday',
            description='Описание тестового сбора для проверки функционала',
            final_price=10000,
            end_date=cls.future_date
        )
        cls.past_date = timezone.now() - timedelta(days=1)
        cls.past_collect = Collect.objects.create(
            author=cls.user,
            title='Завершенный сбор для теста',
            reason='birthday',
            description='Описание завершенного сбора',
            final_price=50000,
            end_date=cls.past_date
        )

    def setUp(self):
        """Настройка клиента для тестов."""
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        """Очистка тестовых данных."""
        super().tearDown()
