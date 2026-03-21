from models import CustomUser
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name',
            'username', 'email'
        ]
        read_only_fields = ['id']


class SMSRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=16)

    def validate_phone(self, attrs):
        if re.fullmatch(r'^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$', attrs):
            return attrs
        return False


class SMSLoginSerializer(SMSRequestSerializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, attrs: str):
        if not attrs.isdigit():
            raise serializers.ValidationError({'error': 'Код должен состоять только из цифр.'})
        return attrs