import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import User


@receiver(post_delete, sender=User)
def delete_profile_photo_file(sender, instance, **kwargs):
    """Delete the file from the filesystem if it exists"""
    if instance.profile_photo:
        if os.path.isfile(instance.profile_photo.path):
            os.remove(instance.profile_photo.path)
