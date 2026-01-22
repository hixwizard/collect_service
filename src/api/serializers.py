from rest_framework.serializers import ModelSerializer

from .models import Payment, Collect


class CollectCreateSerializer(ModelSerializer):
    """Обработка данных создания Группового сбора."""
    class Meta:
        model = Collect
        fields = ('title', 'reason', 'description',
                  'final_price', 'photo', 'end_date'
        )


class CollectDetailSerializer(ModelSerializer):
    class Meta:
        model = Collect
        fields = ('__all__',)


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__',)


class PaymentCreateSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ('amount', 'full_name')