from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from tests.base import BaseTestCase

User = get_user_model()


class UserRegistrationTestCase(BaseTestCase):
    """Тесты для регистрации пользователей."""

    def setUp(self):
        """Настройка для тестов регистрации."""
        super().setUp()
        self.client.force_authenticate(user=None)

    def test_user_registration_success(self):
        """Тест успешной регистрации пользователя."""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@example.com',
            'password': 'newpass123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
