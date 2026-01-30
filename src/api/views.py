from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .email import send_collect_created_email, send_payment_created_email
from .models import Collect, Payment
from .serializers import (
    CollectCreateSerializer,
    CollectDetailSerializer,
    CollectListSerializer,
    PaymentCreateSerializer,
    RegistrationSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """Регистрация пользователей."""

    queryset = User.objects.all()
    http_method_names = ['post']

    def get_serializer_class(self):
        return RegistrationSerializer


class CollectViewSet(ModelViewSet):
    """Создание сбора, список сборов, детальная информация о сборе."""

    queryset = Collect.objects.all()
    http_method_names = ('post', 'get')

    def get_queryset(self):
        """Запрос к связным данным с вычислениями."""
        queryset = Collect.objects.select_related('author')
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('payments__user')
        if self.action == 'list':
            return Collect.objects.order_by('-id')
        return queryset.annotate(
            current_price=Coalesce(Sum('payments__amount'), 0),
            donators_count=Count('payments__user', distinct=True),
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectListSerializer

    def perform_create(self, serializer) -> None:
        collect = serializer.save(author=self.request.user)
        send_collect_created_email(collect)

        cache.delete_pattern('collect_list_*')
        cache.delete_pattern('collect_detail_*')

    def list(self, request, *args, **kwargs):
        """Кэшированный список сборов."""
        cache_key = f'collect_list_page_{request.query_params.get("page", 1)}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 600)
        return response

    def retrieve(self, request, *args, **kwargs):
        """Кэшированная детальная информация о сборе."""
        collect_id = kwargs['pk']
        cache_key = f'collect_detail_{collect_id}'
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, 600)
        return response


class PaymentViewSet(ModelViewSet):
    """Создание пожертвования."""

    queryset = Payment.objects.select_related('collect', 'user')
    model = Payment
    http_method_names = ('post',)

    def get_queryset(self):
        """Запрос к связным объектам."""
        return Payment.objects.select_related('collect', 'user')

    def get_serializer_class(self):
        return PaymentCreateSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        send_payment_created_email(payment)
