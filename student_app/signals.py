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
    
    def banner_update(banner_name):
        is_rarity3 = instance.rarity == 3
        banner = GachaBanner.objects.get(name=banner_name)
        if is_rarity3:
            banner.is_pickup.add(instance)
        else:
            banner.not_pickup.add(instance)
    
    # Comment code 
    is_original = instance.version.name == 'Original'
    is_bunny = instance.version.name == 'Bunny'
    # is_camping = instance.version.name == 'Camping'
    # is_casual = instance.version.name == 'Casual'
    is_cheerleader = instance.version.name == 'Cheerleader'
    # is_dress = instance.version.name == 'Dress'
    # is_loli = instance.version.name == 'Loli'
    # is_maid = instance.version.name == 'Maid'
    is_new_year = instance.version.name == 'New-Year'
    # is_onsen = instance.version.name == 'Onsen'
    # is_riding = instance.version.name == 'Riding'
    is_sport = instance.version.name == 'Sport'
    is_swimsuit = instance.version.name == 'Swimsuit'
    is_xmas = instance.version.name == 'Xmas'
    # is_limited = instance.is_limited

    if is_original:
        for banner in GachaBanner.objects.all():
            banner.not_pickup.add(instance)

    elif is_swimsuit:
        banner_update('Summer Banner')

    elif is_bunny:
        banner_update('Bunny Banner')

    elif is_sport or is_cheerleader:
        banner_update('Sport Banner')
    
    elif is_new_year or is_xmas:
        banner_update('Holiday Banner')
    
    else:
        banner_update('Mixed Banner')