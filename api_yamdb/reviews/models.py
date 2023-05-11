from datetime import datetime
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator)
from django.db import models


class Category(models.Model):
    '''Класс категорий'''

    name = models.CharField(max_length=256)
    slug = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Класс жанров'''

    name = models.CharField(max_length=256)
    slug = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Слаг жанра содержит недопустимый символ'
        )]
    )

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
        validators=[MinValueValidator(0),
                    MaxValueValidator(int(datetime.now().year))],
    )
    description = models.TextField(
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


# class GenreTitle(models.Model):
#     '''Класс произведений'''

#     genre = models.ForeignKey(
#         Genre,
#         on_delete=models.CASCADE
#     )
#     title = models.ForeignKey(
#         Title,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         ordering = ('id',)

#     def __str__(self):
#         return f'{self.title} - {self.genre}'
