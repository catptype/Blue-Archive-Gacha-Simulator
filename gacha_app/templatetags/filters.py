# Read official docs
# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/

from django import template

register = template.Library()

@register.filter(name='get_rate')
def get_rate(obj, rarity):
    return getattr(obj, f'rate_{rarity}_star')
