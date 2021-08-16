from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='category name',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='category slug',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name_plural = 'Categories'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='genre name',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='genre slug',
        max_length=50,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(
        verbose_name='title name',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='year of issue',
    )
    rating = models.IntegerField(
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='title description',
        max_length=1000,
    )
    genre = models.ManyToManyField(
        to=Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        to=Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
