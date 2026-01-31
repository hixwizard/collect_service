from rest_framework.viewsets import ModelViewSet

from .selectors import collect_detail, collect_list, get_users, payment_list
from .serializers import (
    CollectCreateSerializer,
    CollectDetailSerializer,
    CollectListSerializer,
    PaymentCreateSerializer,
    RegistrationSerializer,
)
from .services import collect_create, payment_create


class UserViewSet(ModelViewSet):
    """Регистрация пользователей."""

    queryset = get_users()
    http_method_names = ['post']

    def get_serializer_class(self):
        """Выбор сериализатора."""
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
        """Выбор сериализатора."""
        if self.action == 'create':
            return CollectCreateSerializer
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectListSerializer

    def get_object(self):
        """Получение объекта."""
        return collect_detail(self.kwargs.get('pk'))

    def perform_create(self, serializer) -> None:
        """Создание сбора."""
        collect_data = serializer.validated_data
        collect_data['author'] = self.request.user
        collect_create(collect_data)
        return collect_data


class PaymentViewSet(ModelViewSet):
    """Создание пожертвования."""

    http_method_names = ('post',)

    def get_queryset(self):
        """Запрос к связным объектам."""
        return payment_list()

    def get_serializer_class(self):
        """Выбор сериализатора."""
        return PaymentCreateSerializer

    def perform_create(self, serializer):
        """Создание пожертвования."""
        payment_data = serializer.validated_data
        payment_data['user'] = self.request.user
        payment_create(payment_data)
        return payment_data
