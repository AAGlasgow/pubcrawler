from django import template
from pubcrawl.models import Category

register = template.Library()

@register.inclusion_tag('pubcrawl/cats.html')
def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}
