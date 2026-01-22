from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Payment, Collect


@admin.register(Payment)
class CollectAdmin(admin.ModelAdmin):
    """Панель управления Групповыми сборами."""
    list_display = ('collect', 'user', 'amount', 'created_at',)


@admin.register(Collect)
class PaymentAdmin(admin.ModelAdmin):
    """Панель управления Групповыми сборами."""
    list_display = (
        'author', 'title', 'reason', 'final_price',
        'current_price_display',
        'donators_count_display',
        'end_date',
    )

    def current_price_display(self, obj):
        """Вывод текущей суммы пожертвований."""
        return obj.payments.aggregate(
            total=Coalesce(Sum('amount'), 0)
        )['total']

    def donators_count_display(self, obj):
        """Вывод количества пожертвователей."""
        return obj.payments.values('user').distinct().count()
