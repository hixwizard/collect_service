# flake8: noqa: E501
import random
import sys
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Collect, Payment


class Command(BaseCommand):
    """Генерирует моковые данные."""

    def add_arguments(self, parser):
        """Добавляет аргументы командной строки."""
        parser.add_argument(
            '--users',
            type=int,
            default=1000,
            help='Количество пользователей',
        )
        parser.add_argument(
            '--collects',
            type=int,
            default=5000,
            help='Количество сборов',
        )
        parser.add_argument(
            '--payments',
            type=int,
            default=20000,
            help='Количество платежей',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2000,
            help='Размер батча для bulk_create',
        )

    def handle(self, **options):
        """Генерирует моковые данные."""
        self.stdout.write(self.style.SUCCESS('Генерация моковых данных...'))
        try:
            users = self.create_users(options['users'])
            collects = self.create_collects(options['collects'], users)
            self.create_payments_distributed(
                options['payments'], collects, users, options['batch_size'],
            )
            self.stdout.write(
                self.style.SUCCESS('Генерация моковых данных завершена успешно!'),
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при генерации данных: {str(e)}'),
            )
            raise

    def print_progress(self, current, total, prefix='', suffix='', length=30):
        """Выводит прогресс-бар в консоль."""
        percent = int(100 * (current / float(total)))
        filled = int(length * current // total)
        bar = '*' * filled + '-' * (length - filled)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
        sys.stdout.flush()
        if current == total:
            sys.stdout.write('\n')
            sys.stdout.flush()

    def create_users(self, count):
        """Создает пользователей с мемоизацией имен."""
        self.stdout.write(f'Создаем {count} пользователей...')
        first_names = [
            'Александр', 'Мария', 'Дмитрий', 'Анна', 'Михаил', 'Елена',
            'Артем', 'София', 'Иван', 'Ангелина', 'Алексей', 'Виктория',
            'Максим', 'Ксения', 'Егор', 'Полина', 'Кирилл', 'Алиса',
            'Илья', 'Варвара', 'Никита', 'Евгения', 'Даниил', 'Анастасия',
        ]
        last_names = [
            'Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров',
            'Соколов', 'Михайлов', 'Новиков', 'Федоров', 'Морозов', 'Волков',
            'Алексеев', 'Лебедев', 'Семенов', 'Егоров', 'Павлов', 'Козлов',
            'Степанов', 'Николаев', 'Орлов', 'Андреев', 'Макаров', 'Никитин',
        ]
        existing_count = User.objects.count()
        if existing_count >= count:
            self.stdout.write(f'Используем {existing_count} существующих пользователей')
            return list(User.objects.all()[:count])
        users_to_create = []
        self.stdout.write('Генерируем пользователей...')
        for i in range(existing_count, count):
            if (i - existing_count + 1) % max(1, (count - existing_count) // 10) == 0:
                self.print_progress(
                    i - existing_count + 1,
                    count - existing_count,
                    prefix='Генерация:',
                    suffix='Пользователи',
                )
            user = User(
                username=f'user_{i:06d}',
                email=f'user_{i:06d}@mock.com',
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
            )
            user.set_password('password123')
            users_to_create.append(user)
        if users_to_create:
            self.stdout.write('\nСохраняем пользователей в базу...')
            User.objects.bulk_create(users_to_create, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Создано {len(users_to_create)} новых пользователей'))
        return list(User.objects.all()[:count])

    def create_collects(self, count, users):
        """Создает сборы с весовым распределением."""
        self.stdout.write(f'\nСоздаем {count} сборов...')
        reason_weights = {
            'birthday': 0.4,
            'wedding': 0.3,
            'other': 0.3,
        }
        reasons = list(reason_weights.keys())
        collect_categories = [
            'день рождения', 'свадьбу', 'поездку', 'ремонт', 'покупку',
            'благотворительность', 'образование', 'медицинские расходы',
            'путешествие', 'подарок', 'мероприятие', 'проект',
        ]
        collects_to_create = []
        now = timezone.now()
        self.stdout.write('Генерируем сборы...')
        for i in range(count):
            if (i + 1) % max(1, count // 10) == 0:
                self.print_progress(
                    i + 1,
                    count,
                    prefix='Генерация:',
                    suffix='Сборы',
                )
            category = random.choice(collect_categories)
            title_templates = [
                f'Сбор на {category} #{i:04d}',
                f'Помогите с {category}!',
                f'Сбор средств для {category}',
                f'{category.capitalize()} - нужна помощь!',
                f'Вместе к {category} #{i:04d}',
            ]
            reason = random.choices(reasons, weights=list(reason_weights.values()))[0]
            end_date = now + timedelta(
                days=random.randint(1, 730),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )
            collect = Collect(
                author=random.choice(users),
                title=random.choice(title_templates),
                reason=reason,
                description=f'Сбор средств на {category}. Ваша помощь очень важна для нас! '
                            f'Вместе мы сможем достичь цели. Спасибо всем, кто откликнется!',
                final_price=random.choices(
                    [5000, 10000, 15000, 20000, 25000, 30000],
                    weights=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03],
                )[0],
                end_date=end_date,
            )
            collects_to_create.append(collect)
        self.stdout.write('\nСохраняем сборы в базу...')
        try:
            created_collects = Collect.objects.bulk_create(collects_to_create)
            if created_collects and hasattr(created_collects[0], 'id') and created_collects[0].id:
                self.stdout.write(self.style.SUCCESS(f'Создано {len(created_collects)} сборов'))
                return created_collects
            self.stdout.write(self.style.WARNING('bulk_create не вернул ID, перезагружаем объекты...'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'bulk_create вызвал ошибку: {e}'))
        self.stdout.write('Создаем сборы по одному...')
        created_collects = []
        for i, collect in enumerate(collects_to_create):
            if (i + 1) % max(1, len(collects_to_create) // 10) == 0:
                self.print_progress(
                    i + 1,
                    len(collects_to_create),
                    prefix='Создание:',
                    suffix='Сборы (по одному)',
                )
            created_collect = Collect.objects.create(
                author=collect.author,
                title=collect.title,
                reason=collect.reason,
                description=collect.description,
                final_price=collect.final_price,
                photo=collect.photo,
                end_date=collect.end_date,
            )
            created_collects.append(created_collect)
        self.stdout.write(self.style.SUCCESS(f'Создано {len(created_collects)} сборов'))
        return created_collects

    def create_payments_distributed(self, count, collects, users, batch_size):
        """Создает платежи с реалистичным распределением."""
        self.stdout.write(f'\nСоздаем {count} платежей с распределением...')
        pareto_collects = random.sample(collects, max(1, len(collects) // 5))
        payments_created = 0
        batch_number = 0
        total_batches = (count + batch_size - 1) // batch_size
        while payments_created < count:
            payments_to_create = []
            current_batch_size = min(batch_size, count - payments_created)
            if batch_number % 5 == 0 or payments_created + current_batch_size >= count:
                self.print_progress(
                    min(payments_created + current_batch_size, count),
                    count,
                    prefix='Платежи:',
                    suffix=f'Батч {min(batch_number + 1, total_batches)}/{total_batches}',
                )
            for _ in range(current_batch_size):
                if random.random() < 0.8:
                    collect = random.choice(pareto_collects)
                else:
                    collect = random.choice(collects)
                user = random.choice(users)
                amount = int(random.lognormvariate(4, 1))
                amount = max(50, min(amount, 30000))
                payment = Payment(
                    collect=collect,
                    user=user,
                    amount=amount,
                )
                payments_to_create.append(payment)
            Payment.objects.bulk_create(payments_to_create)
            payments_created += len(payments_to_create)
            batch_number += 1
            if batch_number % 10 == 0:
                self.stdout.write(f'\nОбработано {payments_created}/{count} платежей')
        self.stdout.write(self.style.SUCCESS(f'\nСоздано {payments_created} платежей'))
        self.stdout.write(self.style.SUCCESS('Поля current_price и donators_count вычисляются динамически'))
