from django import template
from django.template.defaultfilters import stringfilter
import markdown as md
from django.utils.html import strip_tags
register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['extra', 'codehilite'])
    
@register.filter()
@stringfilter
def latticeCleaner(value):
    html = md.markdown(value)
    return strip_tags(html)