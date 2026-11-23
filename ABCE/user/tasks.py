import logging
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import CustomUser

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=10)
def send_email_task(self, user_id: int):
    try:
        user = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        logger.warning("User %s not found for password reset email", user_id)
        return

    otp_code = user.generate_otp()

    try:
        send_mail(
            subject="Сброс пароля",
            message=(
                f"Ваш код для сброса пароля: {otp_code}\n"
                f"Код действителен 5 минут. Если вы не запрашивали сброс, просто проигнорируйте это письмо."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("Failed to send OTP email to user %s: %s", user_id, exc)
        # Очищаем код, если все попытки отправки исчерпаны
        if self.request.retries >= self.max_retries:
            user.clear_otp()
            user.save(update_fields=["otp_hash", "otp_created_at", "otp_attempts"])
            raise
        raise self.retry(exc=exc)
