from users.models import User
from rest_framework import serializers
import re


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
