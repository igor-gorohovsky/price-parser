from django import template


register = template.Library()

@register.filter(name='cut_name')
def cut_name(value):
    return value.split('(')[0]
