from rest_framework import serializers
from reviews.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date',)
        read_only_fields = ('pub_date', 'author',)