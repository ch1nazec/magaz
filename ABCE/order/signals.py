from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_notification


@receiver(post_save, sender=Order)
def notify_bot(sender, instance, created, **kwargs):
    if instance.user.telegram_id and instance.total_amount > 0:
        total_str = str(instance.total_amount)
        
        send_order_notification.delay(
            order_id=instance.id,
            telegram_id=instance.user.telegram_id,
            total_amount=total_str
        )