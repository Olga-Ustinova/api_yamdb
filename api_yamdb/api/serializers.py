from django.db.models import Avg

from rest_framework import serializers


from reviews.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):
    '''Сериалайзер для модели Genre'''

    class Meta:
        model = Genre
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    '''Сериалайзер для модели Category'''

    class Meta:
        model = Category
        exclude = ('id',)


class TitleGetRequestSerialize(serializers.ModelSerializer):
    '''Сериалайзер модели Title для безопасных запросов'''

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'discription',
                  'genre',
                  'category')

        def get_rating(self, obj):
            reviews = obj.reviews.all()
            return reviews.aggregate(Avg('score'))['score__avg']


class TitleRequestSerialize(serializers.ModelSerializer):
    '''Сериалайзер модели Title для небезопасных запросов'''

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating', 'discription', 'genre', 'category')

        def get_rating(self, obj):
            reviews = obj.reviews.all()
            return reviews.aggregate(Avg('score'))['score__avg']
