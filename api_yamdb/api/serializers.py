from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.validators import ValidationError
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'bio', 'first_name', 'last_name'
        )


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role',
            'bio', 'first_name', 'last_name'
        )
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UnicodeUsernameValidator(),
        ],
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254
    )

    def create(self, validated_data):
        '''Создание/получение юзера'''
        try:
            user, _ = User.objects.get_or_create(**validated_data)
        except IntegrityError:
            raise ValidationError('Имя пользователя и/или email не валидно')

        return user

    def validate_username(self, value):
        '''Запрет на использование имени "me"'''
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" не валидно')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
