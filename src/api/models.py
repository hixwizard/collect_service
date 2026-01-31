from datetime import datetime

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

    def clean(self) -> None:
        """Валидация модели."""
        super().clean()
        now: datetime = timezone.now()
        if self.end_date < now:
            raise ValidationError(
                'Дата окончания сбора не может быть в прошлом',
            )
        if len(self.title) < 15:
            raise ValidationError(
                'Название сбора должно быть не менее 15 символов',
            )
        if len(self.description) > 10000:
            raise ValidationError(
                'Описание сбора должно быть не менее 10000 символов',
            )
        if self.final_price > 2147483647:
            raise ValidationError(
                'Сумма пожертвования должна быть не более 2147483647',
            )
        max_end_date: datetime = now + timezone.timedelta(days=365)
        if self.end_date < now:
            raise ValidationError(
                'Дата окончания сбора должна быть не менее текущей даты',
            )
        if self.end_date > max_end_date:
            raise ValidationError(
                'Сбор может быть не более года',
            )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Групповой сбор'
        verbose_name_plural = 'Групповые сборы'
        app_label = 'api'


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

    def clean(self) -> None:
        """Минимальная сумма пожертвования."""
        super().clean()
        if self.amount < 100:
            raise ValidationError(
                'Сумма пожертвования должна быть не менее 100 рублей',
            )
        if self.collect.end_date < timezone.now():
            raise ValidationError(
                'Сбор уже завершен',
            )

    def __str__(self) -> str:
        return f'{self.user.username} - {self.amount}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'Пожертвования'
        indexes = [
            models.Index(fields=['collect', 'created_at']),
            models.Index(fields=['user']),
            models.Index(fields=['amount']),
        ]
        app_label = 'api'
