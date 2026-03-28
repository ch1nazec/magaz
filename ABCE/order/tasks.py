from celery import shared_task
from django.conf import settings
import requests


@shared_task
def send_order_notification(order_id, telegram_id, total_amount):
    total_amount = str(total_amount)
    response = requests.post(
        f'{settings.BOT_API_URL}/send_order',
        json={
            'telegram_id': telegram_id,
            'id': order_id,
            'total_amount': total_amount,})