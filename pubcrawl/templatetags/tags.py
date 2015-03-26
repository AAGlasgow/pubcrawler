from django import template

register = template.Library()

@register.inclusion_tag('searchbar.html')
def searchbar(query, cat=None):
    return {'query': query}