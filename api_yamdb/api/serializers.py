from rest_framework import serializers
from reviews.models import Reviews

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field = 'username',
    )
    class Meta:
        model = Reviews,
        field = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('author', 'pub_date',)

    def validate(self, data):
        author = self.context['request'].author
        title = self.context['view'].kwargs['title_id']
        existing_reviews = Reviews.objects.filter(title=title, author=author)
        if existing_reviews.exists():
            raise serializers.ValidationError("Вы уже оставили отзыв.")

        return data