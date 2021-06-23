import datetime

from django import template

register = template.Library()


@register.filter(name='adddate')
def adddate(value, arg):
    return value.replace(value, str((datetime.datetime.now() + datetime.timedelta(days=arg)).strftime('%A %d %B')))

@register.filter(name='split')
def split(value):
    return value.split('/').pop()
