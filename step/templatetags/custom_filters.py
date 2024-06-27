# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''


@register.simple_tag(takes_context=True)
def next_item(context):
    print(context['counter'])
    my_iter = context['counter']
    try:
        return next(my_iter)
    except StopIteration:
        return None
