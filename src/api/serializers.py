from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, IntegerField

from .models import Payment, Collect

User = get_user_model()


class RegistrationSerializer(ModelSerializer):
    """Обработка данных регистрации пользователя."""
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Создание пользователя."""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(ModelSerializer):
    """Обработка данных пользователя."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class PaymentSerializer(ModelSerializer):
    """Обработка данных пожертвования."""
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentForCollectReadSerializer(ModelSerializer):
    """Обработка данных пожертвования для чтения."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ('user', 'amount', 'created_at')


class CollectCreateSerializer(ModelSerializer):
    """Обработка данных создания Группового сбора."""
    class Meta:
        model = Collect
        fields = (
            'title', 'reason', 'description',
            'final_price', 'photo', 'end_date',
            'author'
        )
        read_only_fields = ('author',)


class CollectDetailSerializer(ModelSerializer):
    """
    Обработка данных Группового сбора,
    влючает количество и сумму пожертвований.
    """
    payments = PaymentForCollectReadSerializer(
        many=True, read_only=True
    )
    donators_count = IntegerField(read_only=True)
    current_price = IntegerField(read_only=True)

    class Meta:
        model = Collect
        fields = (
            'author', 'title', 'reason', 'description',
            'final_price', 'current_price', 'photo',
            'donators_count', 'end_date', 'payments'
        )


class CollectListSerializer(ModelSerializer):
    """Обработка данных списка групповых сборов."""

    class Meta:
        model = Collect
        fields = (
            'author', 'title', 'reason', 'description',
            'final_price', 'photo', 'end_date'
        )


class PaymentCreateSerializer(ModelSerializer):
    """Обработка данных создания пожертвования."""

    class Meta:
        model = Payment
        fields = ('collect', 'amount')
