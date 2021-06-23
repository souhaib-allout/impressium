from django import template

register = template.Library()

@register.filter(name='split')
def split(arg,value):
    return value+'hhh'