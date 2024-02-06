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
    
    version_banner_mapping = {
        'Original':     'All Banners',
        'Bunny' :       'Bunny Banner',
        'Camping':      'Casual Banner',
        'Casual':       'Casual Banner',
        'Riding':       'Casual Banner',        
        'Dress':        'Dress Banner',
        'New-Year':     'Holiday Banner',
        'Xmas':         'Holiday Banner',
        'Loli':         'Loli Banner',
        'Maid':         'Maid Banner',
        'Onsen':        'Onsen Banner',
        'Cheerleader':  'Sport Banner',
        'Sport':        'Sport Banner',
        'Swimsuit':     'Summer Banner',
    }

    version_name = instance.version.name
    
    if version_name == 'Original':
        for banner in GachaBanner.objects.all():
            banner.not_pickup.add(instance)
    else:
        banner_name = version_banner_mapping.get(version_name, 'No banner')
        is_rarity3 = instance.rarity == 3
        try:
            banner = GachaBanner.objects.get(name=banner_name)
            if is_rarity3:
                banner.is_pickup.add(instance)
            else:
                banner.not_pickup.add(instance)
        except GachaBanner.DoesNotExist:
            print(f"The version '{version_name}' does not belong to any banner.")