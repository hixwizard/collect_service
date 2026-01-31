from tests.base import BaseTestCase
from api.models import Payment


class PaymentModelTestCase(BaseTestCase):
    """Тесты для модели Payment."""

    def test_payment_creation_success(self):
        """Тест успешного создания пожертвования."""
        payment = Payment.objects.create(
            collect=self.collect,
            user=self.other_user,
            amount=2500
        )
        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.amount, 2500)

    def test_payment_string_representation(self):
        """Тест строкового представления пожертвования."""
        payment = Payment.objects.create(
            collect=self.collect,
            user=self.other_user,
            amount=3000
        )
        expected_str = f'{self.other_user.username} - {3000}'
        self.assertEqual(str(payment), expected_str)

    def test_payment_clean_validation_amount_too_low(self):
        """Тест валидации модели при слишком маленькой сумме."""
        payment = Payment(
            collect=self.collect,
            user=self.other_user,
            amount=50
        )
        with self.assertRaises(Exception):
            payment.full_clean()

    def test_payment_clean_validation_collect_ended(self):
        """Тест валидации модели при завершенном сборе."""
        payment = Payment(
            collect=self.past_collect,
            user=self.other_user,
            amount=1000
        )
        with self.assertRaises(Exception):
            payment.full_clean()
