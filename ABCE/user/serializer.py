from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers, status

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "first_name", "last_name",
            "username", "email", "phone_number",
            "address", "telegram_id",
        ]
        read_only_fields = ["id", "telegram_id"]


class RegistartionUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password], write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name",
            "phone_number", "email", "password", "password_confirm",
        ]

    def validate_email(self, value: str) -> str:
        return value.lower().strip()

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают"},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return CustomUser.objects.create_user(**validated_data)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict):
        email = attrs.get("email", "").lower().strip()
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )

            if not user:
                raise serializers.ValidationError(
                    {"error": "Введите верные данные"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    {"error": "Аккаунт заблокирован"},
                    code=status.HTTP_403_FORBIDDEN,
                )

            attrs["user"] = user
            return attrs

        raise serializers.ValidationError(
            {"error": "Введите логин и пароль"},
            code=status.HTTP_400_BAD_REQUEST,
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "address", "phone_number", "email"]

    def validate_email(self, value: str) -> str:
        return value.lower().strip()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    def validate_old_password(self, value: str) -> str:
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Текущий пароль введён неверно.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "Пароли не совпадают."})
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["password"])
        user.save(update_fields=["password"])
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)

    def validate_email(self, value: str) -> str:
        return value.lower().strip()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    otp_code = serializers.CharField(min_length=6, max_length=6, write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    confirm_password = serializers.CharField(min_length=8, write_only=True)

    def validate_email(self, value: str) -> str:
        return value.lower().strip()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Пароли не совпадают."})

        user = CustomUser.objects.filter(email=attrs["email"]).first()
        try:
            validate_password(attrs["new_password"], user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return attrs
