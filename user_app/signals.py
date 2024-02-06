#from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Achievement, ObtainedAchievement, ObtainedStudent
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
        user = instance.user
        unlocked_achievements = ObtainedAchievement.objects.filter(user=user)
        locked_achievements = Achievement.objects.all().exclude(id__in=unlocked_achievements.values('achievement_id'))

        # Check which achivement can be unlocked
        for achievement in locked_achievements:
            required_students = achievement.criteria.all()
            unlock_condition = True

            # Skip this locked achievement when user does not obtain student
            for student in required_students:
                if not ObtainedStudent.objects.filter(student=student).exists():
                    unlock_condition = False
                    break
            
            if unlock_condition:
                ObtainedAchievement.objects.create(
                    user=user, 
                    achievement=achievement,
                )