import re

from django.db.models import Avg
from rest_framework import serializers, status
from reviews.models import Categorie, Comment, Genre, Review, Title
from users.models import User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        read_only_fields = ('id', 'role')

    def validate(self, data):
        username = data.get('username')
        if username and not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                'Поле username не соответствует паттерну',
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate(self, data):
        username = data.get('username')
        if username and not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                'Поле username не соответствует паттерну',
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return data


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        username = data.get('username')
        if username and not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
                'Поле username не соответствует паттерну',
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено')
        return data


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        exclude = ('id',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorieSerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Categorie.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = (
            'author',
            'pub_date',
        )

    def validate(self, data):
        author = data.get('author')
        title = self.context['view'].kwargs['title_id']
        existing_reviews = Review.objects.filter(title=title, author=author)
        if existing_reviews.exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв.",
                code='invalid',
                status=status.HTTP_400_BAD_REQUEST,
            )

        return data
