from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint

from api.validators import year_validator
from users.models import CustomUser as User


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='категория')
    slug = models.SlugField(unique=True, verbose_name='slug категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name='жанр')
    slug = models.SlugField(unique=True, verbose_name='slug жанра')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='произведение', db_index=True
    )
    year = models.IntegerField(
        validators=[year_validator], verbose_name='год выпуска',
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        blank=True, null=True, verbose_name='категория',
        db_index=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', verbose_name='жанр',
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание', blank=True, null=True
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                1,
                'Значение должно быть целым чиилом больше 0'
            ),
            MaxValueValidator(
                10,
                'Значение должно быть целым числом меньше 11'
            )
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('author', 'title',), name='unique_review'
            ),
        )
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
