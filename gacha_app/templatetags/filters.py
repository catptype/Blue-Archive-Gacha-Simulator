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



@register.filter(name='subtract_rate')
def subtract_rate(value1, value2):
    return value1 - value2

@register.filter(name='divide_rate')
def divide_rate(value1, value2):
    result = value1 / value2
    return round(result, 4)