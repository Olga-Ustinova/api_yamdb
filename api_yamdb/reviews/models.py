from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

MAX_CATEGORY_LENGTH = 256
MAX_GENRE_LENGTH = 256
MAX_TITLE_NAME_LENGTH = 256
MIN_SCORE_NAME = 1
MAX_SCORE_NAME = 10
MAX_CHAR_LENGTH_TO_REVIEW = 15
MAX_CHAR_LENGTH_TO_COMMENT = 15


class Category(models.Model):
    """Класс категорий"""

    name = models.CharField(
        max_length=MAX_CATEGORY_LENGTH,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_GENRE_LENGTH,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_TITLE_NAME_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(int(datetime.now().year))],
        verbose_name='Год релиза'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
        verbose_name='Жанры'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE_NAME),
            MaxValueValidator(MAX_SCORE_NAME)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_title_user_author'),
        ]

    def __str__(self):
        return self.text[:MAX_CHAR_LENGTH_TO_REVIEW]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст коментария')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:MAX_CHAR_LENGTH_TO_COMMENT]
