from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Collect(models.Model):
    """Модель Группового денежного сбора."""

    REASON_CHOICE = [
        ('birthday', 'День Рождения'),
        ('wedding', 'Свадьба'),
        ('other', 'Другой'),
    ]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Автор сбора',
    )
    title = models.CharField(
        blank=False,
        null=False,
        max_length=100,
        verbose_name='Название сбора',
    )
    reason = models.CharField(
        choices=REASON_CHOICE,
        default='other',
        max_length=20,
        verbose_name='Повод сбора',
    )
    description = models.TextField(
        max_length=10000,
        blank=False,
        null=False,
        verbose_name='Описание',
    )
    final_price = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='Сколько запланировано собрать',
    )
    photo = models.ImageField(
        upload_to='payment_photo',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )
    end_date = models.DateTimeField(verbose_name='Дата окончания сбора')

    def __str__(self) -> str:
        return self.title

    def validatr_end_date(self) -> None:
        """Валидация даты окончания сбора."""
        if self.end_date < timezone.now():
            raise ValidationError(
                'Дата окончания сбора не может быть в прошлом',
            )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Групповой сбор'
        verbose_name_plural = 'Групповые сборы'


class Payment(models.Model):
    """Модель пожертвования."""

    collect = models.ForeignKey(
        Collect,
        on_delete=CASCADE,
        related_name='payments',
        verbose_name='Название сбора',
    )
    user = models.ForeignKey(
        User, on_delete=CASCADE,
        related_name='user_payments',
        verbose_name='Имя пользователя в системе',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма пожертвования',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'
        indexes = [
            models.Index(fields=['collect', 'created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['amount']),
        ]

    def minimum_amount(self) -> None:
        """Минимальная сумма пожертвования."""
        if self.amount < 100:
            raise ValidationError(
                'Сумма пожертвования должна быть не менее 100 рублей',
            )

    def validate_collect_time(self) -> None:
        """Валидация времени сбора."""
        if self.collect.end_date < timezone.now():
            raise ValidationError(
                'Сбор уже завершен',
            )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.amount}'
