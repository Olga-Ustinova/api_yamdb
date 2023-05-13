from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    title = SlugRelatedField(read_only=True, slug_field='name')
    author = SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Review

    validators = [UniqueTogetherValidator(queryset=Review.objects.all(),
                                          fields=('author', 'title'))]

    def validate_score(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на данное произведение')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment
