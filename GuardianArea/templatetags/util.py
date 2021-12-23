from django import template

register = template.Library()

@register.filter
def get_type(value):
    return type(value)

@register.filter
def get_note(value, arg):
    # print(value)
    # print(value[arg])
    for i in value:
        if str(i) == str(arg):
            return value[i]
