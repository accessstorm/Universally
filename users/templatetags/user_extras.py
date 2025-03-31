from django import template

register = template.Library()

@register.filter(name='split')
def split_string(value, arg):
    """
    Splits the string by the specified delimiter.
    Usage: {{ some_string|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(arg)]
    return []

# You can add other user-specific template tags or filters here
