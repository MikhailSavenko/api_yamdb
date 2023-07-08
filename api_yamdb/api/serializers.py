from users.models import Users
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Users
        fields = ('id', 'email', 'username', 'role', 'bio', 'first_name', 'last_name')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data