from django.shortcuts import get_object_or_404
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Avg
from django.db.utils import IntegrityError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    '''Сериалайзер для модели Category'''

    class Meta:
        model = Category
        exclude = ('id',)


class TitleReadRequestSerialize(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score'))['rating']


class TitleWriteRequestSerialize(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score'))['rating']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UnicodeUsernameValidator(),
        ],
        max_length=150,
    )
    email = serializers.EmailField(max_length=254)

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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'score', 'pub_date', 'text')
        model = Review

    def validate_score(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return value

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            author = request.user
            title_id = self.context['view'].kwargs.get("title_id")
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(author=author).exists():
                raise ValidationError('Можно оставить только один отзыв')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'pub_date', 'text')
        model = Comment
