from django.urls import reverse
from rest_framework import status

from api.models import Payment
from tests.base import BaseTestCase


class PaymentViewSetTestCase(BaseTestCase):
    """Тесты для ViewSet пожертвований."""

    def setUp(self):
        """Настройка тестовых данных для пожертвований."""
        super().setUp()

    def test_create_payment_success(self):
        """Тест успешного создания пожертвования."""
        url = reverse('payment-list')
        data = {
            'collect': self.collect.pk,
            'amount': 5000,
        }
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(amount=5000).exists())

    def test_create_payment_validation_error_amount_too_low(self):
        """Тест ошибки валидации при слишком маленькой сумме."""
        url = reverse('payment-list')
        data = {
            'collect': self.collect.pk,
            'amount': 50,
        }
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(
            'Сумма пожертвования не менее 100 рублей' in str(response.data),
        )

    def test_create_payment_validation_error_author_cannot_donate(self):
        """Тест ошибки валидации при попытке автора пожертвовать себе."""
        url = reverse('payment-list')
        data = {
            'collect': self.collect.pk,
            'amount': 1000,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_validation_error_collect_ended(self):
        """Тест ошибки валидации при завершенном сборе."""
        url = reverse('payment-list')
        data = {
            'collect': self.past_collect.pk,
            'amount': 1000,
        }
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
