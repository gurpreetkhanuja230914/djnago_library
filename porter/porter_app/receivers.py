from django.dispatch import receiver
from .signals import user_logged_in

@receiver(user_logged_in)
def handle_user(sender,**kwargs):
    print("receiver handle_user fnction")
    pass