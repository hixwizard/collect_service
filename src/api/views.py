from django.db.models import Count, Sum
from django.contrib.auth import get_user_model
from django.db.models.functions import Coalesce
from rest_framework.viewsets import ModelViewSet

from .models import Collect, Payment
from .serializers import (
    CollectCreateSerializer, CollectDetailSerializer, CollectListSerializer,
    PaymentCreateSerializer,
    RegistrationSerializer
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
        return (
            Collect.objects
            .annotate(
                current_price=Coalesce(Sum('payments__amount'), 0),
                donators_count=Count('payments__user', distinct=True)
            )
            .select_related('author')
            .prefetch_related('payments__user')
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectListSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PaymentViewSet(ModelViewSet):
    """Создание пожертвования."""
    queryset = Payment.objects.select_related('collect', 'user')
    model = Payment
    http_method_names = ('post', 'get')

    def get_serializer_class(self):
        return PaymentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
