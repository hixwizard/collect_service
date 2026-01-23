from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.serializers import ModelSerializer, IntegerField
from rest_framework.exceptions import ValidationError
from drf_extra_fields.fields import Base64ImageField

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
    photo = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Collect
        fields = (
            'title', 'reason', 'description',
            'final_price', 'photo', 'end_date',
            'author'
        )
        read_only_fields = ('author',)

    def validate(self, data):
        """Валидация данных Группового сбора."""
        title = data.get('title')
        description = data.get('description')
        final_price = data.get('final_price')
        end_date = data.get('end_date')
        if len(title) < 15:
            raise ValidationError(
                'Название сбора должно быть не менее 15 символов'
            )
        if len(description) > 10000:
            raise ValidationError(
                'Описание сбора должно быть не менее 10000 символов'
            )
        if final_price > 2147483647:
            raise ValidationError(
                'Сумма пожертвования должна быть не более 2147483647'
            )
        time = timezone.now()
        max_end_date = time + timezone.timedelta(days=365)
        if end_date < time:
            raise ValidationError(
                'Дата окончания сбора должна быть не менее текущей даты'
            )
        if end_date > max_end_date:
            raise ValidationError(
                'Сбор может быть не более года'
            )
        return data


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

    def validate(self, data):
        """Общая проверка данных."""
        collect = data.get('collect')
        amount = data.get('amount')
        request = self.context.get('request')
        user = request.user
        if collect.end_date < timezone.now():
            raise ValidationError('Групповой сбор уже завершен')
        if amount < 100:
            raise ValidationError('Сумма пожертвования не менее 100 рублей')
        if collect.author == user:
            raise ValidationError('Вы не можете пожертвовать самому себе')
        return data
