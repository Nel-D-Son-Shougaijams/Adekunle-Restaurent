from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram_bot import send_order_notification

@receiver(post_save,sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        print("hello")
        send_order_notification(instance)