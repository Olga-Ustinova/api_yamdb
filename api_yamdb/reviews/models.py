from datetime import datetime
from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    '''Класс категорий'''

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Класс жанров'''

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Класс произведений'''

    name = models.CharField(
        max_length=256
    )
    year = models.IntegerField(
        validators=[MaxValueValidator(int(datetime.now().year))]
    )
    description = models.TextField(
        blank=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    '''Класс произведений'''

    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} - {self.genre}'
