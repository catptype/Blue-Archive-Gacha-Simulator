# Read official docs
# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/

from django import template

register = template.Library()

@register.filter(name='percentage')
def divide_rate(value1, value2):
    result = (value1 / value2) * 100
    return round(result, 2)