from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Student
from gacha_app.models import GachaBanner

@receiver(pre_save, sender=Student)
def remove_student_from_banner(sender, instance, **kwargs):
    for banner in GachaBanner.objects.all():
        if banner.not_pickup.filter(pk=instance.pk).exists():
            banner.not_pickup.remove(instance)
        elif banner.is_pickup.filter(pk=instance.pk).exists():
            banner.is_pickup.remove(instance)

@receiver(post_save, sender=Student)
def add_student_to_banner(sender, instance, created, **kwargs):
    is_low_rarity = instance.rarity < 3
    is_rarity3 = instance.rarity == 3
    is_r3_original = instance.version.name == 'Original' and is_rarity3
    is_r3_swimsuit = instance.version.name == 'Swimsuit' and is_rarity3
    is_r3_bunny = instance.version.name == 'Bunny' and is_rarity3
    is_r3_sport = instance.version.name == 'Sport' and is_rarity3
    is_r3_cheer = instance.version.name == 'Cheerleader' and is_rarity3

    if is_low_rarity or is_r3_original:
        for banner in GachaBanner.objects.all():
            banner.not_pickup.add(instance)
    
    elif is_r3_swimsuit:
        banner = GachaBanner.objects.get(name='Swimsuit Banner')
        banner.is_pickup.add(instance)

    elif is_r3_bunny:
        banner = GachaBanner.objects.get(name='Bunny Banner')
        banner.is_pickup.add(instance)

    elif is_r3_sport or is_r3_cheer:
        banner = GachaBanner.objects.get(name='Sport Banner')
        banner.is_pickup.add(instance)

    elif instance.is_limited:
        banner = GachaBanner.objects.get(name='Limited Banner')
        banner.is_pickup.add(instance)