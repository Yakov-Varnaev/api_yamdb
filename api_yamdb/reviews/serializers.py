from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Review, Comment, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        required=False,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        exclude = ('title',)

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            title = get_object_or_404(
                Title,
                pk=self.context['view'].kwargs.get('title_id')
            )
            if Review.objects.filter(
                author=self.context['request'].user,
                title=title
            ).exists():
                raise serializers.ValidationError(
                    detail=f'You have already reviewed {title.name}'
                )
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
