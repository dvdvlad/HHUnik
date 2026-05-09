from django import template
from django.template.defaultfilters import stringfilter
import markdown as md
import re
register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['extra', 'codehilite'])
    
@register.filter()
@stringfilter
def latticeCleaner(value):
    return re.sub(r"[#*]","",value)