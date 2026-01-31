from django.db import transaction

from .cache import (
    invalidate_collect_detail_cache,
    invalidate_collect_list_cache,
)
from .email import send_collect_created_email, send_payment_created_email
from .models import Collect, Payment


@transaction.atomic
def collect_create(collect_data) -> Collect:
    """Создание нового сбора."""
    collect = Collect(**collect_data)
    collect.full_clean()
    collect.save()
    send_collect_created_email(collect)
    invalidate_collect_list_cache()
    return collect


@transaction.atomic
def payment_create(payment_data) -> Payment:
    """Создание нового пожертвования."""
    payment = Payment(**payment_data)
    payment.full_clean()
    payment.save()
    send_payment_created_email(payment)
    invalidate_collect_detail_cache(payment.collect.id)
    invalidate_collect_list_cache()
    return payment
