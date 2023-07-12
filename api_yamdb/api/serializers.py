from users.models import User
from rest_framework import serializers
import re
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Categorie, Genre, Title


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'bio', 'first_name', 'last_name')
        read_only_fields = ('id', 'role')

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if username and not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError(
            'Поле username не соответствует паттерну'
        )
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'bio', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


class UserSignUpSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'username')
    
    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
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
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
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

