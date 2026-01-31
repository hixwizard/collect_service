from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .services import collect_create, payment_create
from .selectors import collect_list, collect_detail, get_users, payment_list
from .serializers import (
    CollectCreateSerializer,
    CollectDetailSerializer,
    CollectListSerializer,
    PaymentCreateSerializer,
    RegistrationSerializer,
)


class UserViewSet(ModelViewSet):
    """Регистрация пользователей."""

    queryset = get_users()
    http_method_names = ['post']

    def get_serializer_class(self):
        return RegistrationSerializer


class CollectViewSet(ModelViewSet):
    """Создание сбора, список сборов, детальная информация о сборе."""

    http_method_names = ('post', 'get')

    def get_queryset(self):
        """Запрос к связным данным с вычислениями."""
        if self.action == 'retrieve':
            return collect_detail()
        return collect_list()

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectListSerializer

    def get_object(self):
        return collect_detail(self.kwargs.get('pk'))

    def perform_create(self, serializer) -> None:
        collect_data = serializer.validated_data
        collect_data['author'] = self.request.user
        collect_create(collect_data)
        return collect_data

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

    http_method_names = ('post',)

    def get_queryset(self):
        """Запрос к связным объектам."""
        return payment_list()

    def get_serializer_class(self):
        return PaymentCreateSerializer

    def perform_create(self, serializer):
        payment_data = serializer.validated_data
        payment_data['user'] = self.request.user
        payment_create(payment_data)
        return payment_data
