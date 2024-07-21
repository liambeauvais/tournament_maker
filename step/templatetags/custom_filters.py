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
    my_iter = context['counter']
    try:
        return next(my_iter)
    except StopIteration:
        return None


@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)
