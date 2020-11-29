from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def parse(dic,i):
    print("FILTER",dic,i)
    return dic[i]
