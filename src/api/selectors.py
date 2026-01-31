from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce

from .models import Collect, Payment
from .cache import (
    cache_key_for_collect_list,
    cache_key_for_collect_detail,
    cache_collect_list,
    cache_collect_detail,
)

User = get_user_model()


def get_users():
    """Получение пользователя по ID."""
    return User.objects.all()


def collect_list():
    """Получение списка сборов с вычислениями."""
    return Collect.objects.all().order_by('-id')


def collect_detail(id):
    """Получение детальной информации о сборе."""
    return Collect.objects.select_related('author').prefetch_related(
        'payments__user').annotate(
        current_price=Coalesce(Sum('payments__amount'), 0),
        donators_count=Count('payments__user', distinct=True),
    ).get(id=id)


def payment_list():
    """Получение списка пожертвований для сбора."""
    return Payment.objects.select_related('user').order_by('-created_at')


def collect_get(id):
    """Получение сбора по ID."""
    return Collect.objects.get(id=id)


