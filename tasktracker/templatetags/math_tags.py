from django import template

register = template.Library()

@register.filter(name='mult')
def mult(value, arg):
    return value * arg

@register.filter(name='trim')
def trim(value):
    int_val = value.split(':')[0]
    return(int(int_val))

