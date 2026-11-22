from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from .models import CustomUser


@shared_task
def send_email_task(user_id):
    user = CustomUser.objects.get(pk=user_id)
    otp_code = user.generate_otp()

    send_mail(
        subject="Reset your password",
        message=f"Ваш код: {otp_code}. Если вы не отправляли код, то проигнорируйте сообщение.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
