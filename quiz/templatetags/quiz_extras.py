from django import template

register = template.Library()

@register.filter(name='is_list')
def is_list(value):
    """Checks if a value is an instance of a list."""
    return isinstance(value, list)

# You can add other useful filters here later, e.g., for formatting
