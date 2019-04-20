import uuid
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


def uuid_str():
    return ''.join(str(uuid.uuid4()).split('-'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jwt_secret = models.CharField(max_length=32, default=uuid_str)
    phone_number = models.CharField(max_length=12)
    name = models.CharField(max_length=50)
    language = models.CharField(choices=settings.LANGUAGE_CHOICES, max_length=4)
    currency = models.CharField(choices=settings.CURRENCY_CHOICES, max_length=4)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
