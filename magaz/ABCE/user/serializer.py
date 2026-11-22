from .models import CustomUser
from rest_framework import serializers, status
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import re


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'last_name',
            'username', 'email', 'phone_number',
            'address', 'telegram_id',
        ]
        read_only_fields = ['id']


class RegistartionUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        validators=[validate_password],
        write_only=True)
    password_confirm = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name',
            'phone_number', 'email', 'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'error': 'Пароли не совпадают'},
                                              code=status.HTTP_400_BAD_REQUEST)
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs: dict):
        email = attrs.get('email'); password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password)
            
            if not user:
                raise serializers.ValidationError({'error': 'Введите верные данные'}, code=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                raise serializers.ValidationError({'error': 'Аккаунт заблокирован'}, code=status.HTTP_403_FORBIDDEN)
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                {'error': 'Введите логин и пароль',}, code=status.HTTP_400_BAD_REQUEST)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'telegram_id', 'phone_number', 'email']

    def update(self, instance, validated_data: dict):
        for attr, values in validated_data.items():
            setattr(instance, attr, values)
        instance.save()

        return instance


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            return serializers.ValidationError({"error": 'Пароли не совпадают'},
                                               code=status.HTTP_400_BAD_REQUEST)
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['password_confirm'])

        user.save()
        return user


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




class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)
    otp_code = serializers.CharField(min_length=6, write_only=True)

    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)


    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})

        try:
            user = CustomUser.objects.get(email=attrs["email"])
            validate_password(attrs['new_password'], user=user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return attrs