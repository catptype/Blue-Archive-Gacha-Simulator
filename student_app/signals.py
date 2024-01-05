#from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Student
from gacha_app.models import GachaBanner

@receiver(post_save, sender=Student)
def add_student_to_not_pickup(sender, instance, created, **kwargs):
    if created and instance.rarity < 3:
        # Add the new student to the not_pickup field of all GachaBanners
        for gacha_banner in GachaBanner.objects.all():
            gacha_banner.not_pickup.add(instance)
