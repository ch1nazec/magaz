from models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name',
            'username', 'email'
        ]
        read_only_fields = ['id']