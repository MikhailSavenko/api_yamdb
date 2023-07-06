from users.models import Users
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'email', 'username')