from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

from titles.models import Title

User = get_user_model()


class Review(models.Model):
    title = models.ForeignKey(
        verbose_name='title',
        to=Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='review text',
    )
    author = models.ForeignKey(
        verbose_name='review author',
        to=User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        verbose_name=' authors mark',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(
        verbose_name='comment text'
    )
    author = models.ForeignKey(
        verbose_name='comment author',
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        verbose_name='date of publication',
        auto_now_add=True)
    review = models.ForeignKey(
        verbose_name='comment to review',
        to=Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
