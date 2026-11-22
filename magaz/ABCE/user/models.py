import secrets

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.contrib.auth.hashers import make_password, check_password

from datetime import timedelta


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)

    phone_regex = RegexValidator(
        regex=r'^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
        message="Номер должен быть в формате: +7 (999) 123-45-67 или 89991234567"
    )
    phone_number = models.CharField(
        max_length=16,
        unique=True,
        verbose_name='Номер телефона',
        validators=[phone_regex], null=True, blank=True
    )
    address = models.TextField(
        max_length=500,
        verbose_name='Адрес доставки',
        blank=True,
        null=True,
    )
    telegram_id = models.BigIntegerField(verbose_name='Айди тг пользователя', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    otp_hash = models.CharField(max_length=128, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.PositiveSmallIntegerField(default=0)

    OTP_TTL = timedelta(minutes=5)
    MAX_ATTEMPTS = 5

    def __str__(self):
        return self.username or self.phone_number or self.email or f"User {self.id}"

    def generate_otp(self):
        code = f'{secrets.randbelow(1_000_000):06d}'
        self.otp_hash = make_password(code)
        self.otp_created_at = timezone.now()

        self.otp_attempts = 0
        self.save(update_fields=['otp_hash', 'otp_created_at', 'otp_attempts'])
        print(code)
        return code

    def verify_otp(self, code: str) -> bool:
        if not self.otp_hash or not self.otp_created_at:
            return False
        if timezone.now() - self.otp_created_at > self.OTP_TTL:
            return False
        if self.otp_attempts >= self.MAX_ATTEMPTS:
            return False

        if check_password(code, self.otp_hash):
            return True

        self.otp_attempts += 1
        self.save(update_fields=['otp_attempts'])
        return False

    def clear_otp(self):
        self.otp_hash = None
        self.otp_created_at = None
        self.otp_attempts = 0

    

class OTPCode(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)