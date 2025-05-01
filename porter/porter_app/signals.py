from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Order)
def send_status_update(sender, instance, created, **kwargs):
    # Only send if status is updated (not just created)
    if not created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"booking_{instance.id}",
            {
                "type": "booking_status_update",
                "status": instance.status,
            }
        )
