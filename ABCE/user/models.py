from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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
        validators=[phone_regex]
    )
    address = models.TextField(
        max_length=500,
        verbose_name='Адрес доставки',
        blank=True,
        null=True,
    )
    telegram_id = models.PositiveIntegerField(verbose_name='Айди тг пользователя', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username or self.phone_number or self.email or f"User {self.id}"
    

class OTPCode(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)