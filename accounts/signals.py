# SIGNALS
from django.db.models.signals import post_save
from django.dispatch import receiver

#MODELS
from .models import (
    User,
    UserProfile
)
@receiver(post_save, sender=User)
def create_userProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
       
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
