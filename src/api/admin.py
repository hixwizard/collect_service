from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import Coalesce

from .models import Collect, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Панель управления Пожертвованиями."""

    list_display = ('id', 'collect', 'user', 'amount', 'created_at')
    list_filter = ('created_at', 'collect')
    search_fields = ('user__username', 'collect__title')


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Панель управления Групповыми сборами."""

    list_display = (
        'id', 'author', 'title', 'reason', 'final_price',
        'current_price_display',
        'donators_count_display',
        'end_date',
    )
    list_filter = ('reason', 'end_date')
    search_fields = ('author__username', 'title')

    def current_price_display(self, obj):
        """Вывод текущей суммы пожертвований."""
        return obj.payments.aggregate(
            total=Coalesce(Sum('amount'), 0),
        )['total']

    def donators_count_display(self, obj):
        """Вывод количества пожертвователей."""
        return obj.payments.values('user').distinct().count()

    donators_count_display.short_description = 'Количество пожертвований'
    donators_count_display.admin_order_field = 'donators_count'
    current_price_display.short_description = 'Собрано'
    current_price_display.admin_order_field = 'current_price'
