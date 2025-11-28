from django import template

register = template.Library()

@register.filter
def split(value, key=','):
    """Divide una cadena por comas y elimina espacios extra."""
    if not value:
        return []
    return [item.strip() for item in value.split(key)]
