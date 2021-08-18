from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from .models import Review, Comment
from titles.models import Title


# В общем на сколько я посмотрю там не так много нужно будет сделать
# 2. Я так и не нашел требования, чтобы тут был unique constraints, поэтому давай
#    просто уберем всю эту историю
# class ReviewGetSerializer(serializers.ModelSerializer): # 1. Не все поля участвуют в ответе, надо подумать, какое поле надо исключить
#     author = SlugRelatedField(
#         slug_field='username',
#         read_only=True,
#         required=False
#         # default=serializers.CurrentUserDefault() RRRRRRRRRRRRRRRRRRRRRRRRRRrr
#     )

#     class Meta:
#         model = Review
#         exclude = ('title',)


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = SlugRelatedField(
        slug_field='id',
        required=False,
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=('title', 'author')
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
