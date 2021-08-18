from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from django.db.models import Avg

from .models import Review, Comment


# В общем на сколько я посмотрю там не так много нужно будет сделать
# 1. Не все поля участвуют в ответе, надо подумать, какое поле надо исключить
# 2. Я так и не нашел требования, чтобы тут был unique constraints, поэтому давай
#    просто уберем всю эту историю

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = SlugRelatedField(
        slug_field='id',
        required=False,
        read_only=True
    )

    class Meta:
        # 3. Давай будем указывать сначала модель,
        # а потом уже поля, будет удобнее читать код
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author')
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    review = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
