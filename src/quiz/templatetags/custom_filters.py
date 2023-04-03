from django import template

register = template.Library()


@register.filter
def negative(value):
    return -value


@register.filter
def multi(value, arg):
    return value * arg


@register.filter
def dived(value, arg):
    return value // arg


@register.filter
def calc_point(v1, v2):
    return max(0, v1 - v2)
