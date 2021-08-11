from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


class Titles(models.Model):
    pass


class Reviews(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE, ralated_name='reviews')
    score = models.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE, ralated_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
