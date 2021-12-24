from django import template
import re
from django_currentuser.middleware import get_current_user
register = template.Library()

@register.filter
def get_type(value):
    return type(value)

@register.filter
def get_note(value, arg):
    # print(value)
    # print(value[arg])
    try:
        for i in value:
            if str(i) == str(arg):
                return value[i]
    except:
        return ''



@register.filter
def remove_username(value):
    return value.replace('('+str(get_current_user())+')', '')
