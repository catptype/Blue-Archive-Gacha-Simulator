#from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ObtainedStudent
from gacha_app.models import GachaTransaction

@receiver(post_save, sender=GachaTransaction)
def update_collection(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        student = instance.student

        if not ObtainedStudent.objects.filter(user=user, student=student).exists():
            ObtainedStudent.objects.create(
                user=user, 
                student=student,
            )

@receiver(post_save, sender=ObtainedStudent)
def update_achievement(sender, instance, created, **kwargs):
    if created:
        pass