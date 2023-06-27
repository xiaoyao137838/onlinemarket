from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def post_save_create_userprofile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except Exception as e: 
            logger.error(e)
            UserProfile.objects.create(user=instance)