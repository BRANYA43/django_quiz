from django import template

register = template.Library()


@register.simple_tag
def expression(value: str, *args):
    print(args)
    print(value.format(*args))
    return eval(value.format(*args))
