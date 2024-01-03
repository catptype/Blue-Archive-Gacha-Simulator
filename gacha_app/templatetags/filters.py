# Read official docs
# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/

from django import template

register = template.Library()

@register.filter(name='get_rate')
def get_rate(obj, rarity):
    return getattr(obj, f'r{rarity}_rate')

@register.filter(name='filter_rarity')
def filter_rarity(obj, rarity):
    return obj.filter(rarity=rarity)
