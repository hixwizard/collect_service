from rest_framework.viewsets import ModelViewSet

from .models import Collect, Payment
from .serializers import (
    CollectCreateSerializer, PaymentCreateSerializer, PaymentSerializer,
    CollectDetailSerializer, CollectListSerializer
)


class CollectViewSet(ModelViewSet):
    queryset = Collect.objects.all()
    model = Collect
    http_method_names = ('post', 'get')

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectCreateSerializer
        if self.action == 'retrieve':
            return CollectDetailSerializer
        return CollectListSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    model = Payment
    http_method_names = ['post']

    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

