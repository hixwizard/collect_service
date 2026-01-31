from datetime import timedelta
from random import choice, randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Collect, Payment

User = get_user_model()


class Command(BaseCommand):
    """Создание моковых данных."""

    def add_arguments(self, parser):
        """Аргументы командной строки."""
        parser.add_argument('--users', type=int, default=1000)
        parser.add_argument('--collects', type=int, default=5000)
        parser.add_argument('--payments', type=int, default=20000)

    def handle(self, **options):
        """Основной обработчик."""
        users = []
        for i in range(options['users']):
            user = User(
                username=f'пользователь {i}',
                email=f'test_user{i}@test.com',
                first_name=f'Имя {i}',
                last_name=f'Фамилия {i}',
            )
            user.set_password('1')
            users.append(user)
        User.objects.bulk_create(users, ignore_conflicts=True)
        users = list(User.objects.filter(email__startswith='test_user'))

        collects = []
        reasons = ['birthday', 'wedding', 'other']
        now = timezone.now()
        for i in range(options['collects']):
            collect = Collect(
                author=choice(users),
                title=f'Сбор {i}',
                reason=choice(reasons),
                description='Тестовое описание сбора',
                final_price=randint(5000, 30000),
                end_date=now + timedelta(days=randint(1, 365)),
            )
            collects.append(collect)
        created_collects = Collect.objects.bulk_create(collects)

        payments = []
        for i in range(options['payments']):
            payment = Payment(
                collect=choice(created_collects),
                user=choice(users),
                amount=randint(100, 10000),
            )
            payments.append(payment)
        Payment.objects.bulk_create(payments)
        self.stdout.write(self.style.SUCCESS('Данные успешно созданы'))
