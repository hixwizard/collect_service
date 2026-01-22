from django.contrib import admin
from .models import Payment, Collect


@admin.register(Payment)
class CollectAdmin(admin.ModelAdmin):
    """Панель управления Групповыми сборами."""
    list_display = ('collect', 'user', 'amount', 'created_at', 'full_name',)


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    """Панель управления Групповыми сборами."""
    list_display = (
        'author', 'title', 'reason', 'description',
        'final_price', 'current_price', 'photo',
        'donators_count', 'end_date',
    )
