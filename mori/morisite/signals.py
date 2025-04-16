from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Album, Trash, Like, Avatar

@receiver(post_save, sender=User)
def create_user_album(sender, instance, created, **kwargs):
    if created:
        Album.objects.create(user=instance, title=f'Tất cả', is_main=True)
        Avatar.objects.create(user=instance)