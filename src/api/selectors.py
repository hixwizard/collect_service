from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.http import Http404

from .cache import (
    cache_collect_detail,
    cache_collect_list,
)
from .models import Collect, Payment

User = get_user_model()


def get_users():
    """Получение пользователя по ID."""
    return User.objects.all()


def collect_list():
    """Получение списка сборов с вычислениями."""
    cache_data = cache_collect_list()
    if cache_data is not None:
        return cache_data
    data = Collect.objects.all().order_by('-id')
    cache_collect_list(data)
    return data


def collect_detail(collect_id):
    """Получение детальной информации о сборе."""
    cache_data = cache_collect_detail(collect_id)
    if cache_data is not None:
        return cache_data
    try:
        data = Collect.objects.select_related('author').prefetch_related(
            'payments__user').annotate(
            current_price=Coalesce(Sum('payments__amount'), 0),
            donators_count=Count('payments__user', distinct=True),
        ).get(id=id)
        cache_collect_detail(id, data)
        return data
    except Collect.DoesNotExist:
        raise Http404('Сбор не найден')


def payment_list():
    """Получение списка пожертвований для сбора."""
    return Payment.objects.select_related('user').order_by('-created_at')


def collect_get(collect_id):
    """Получение сбора по ID."""
    try:
        return Collect.objects.get(id=collect_id)
    except Collect.DoesNotExist:
        raise Http404('Сбор не найден')
