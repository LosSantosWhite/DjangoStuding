from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='get_atr')
@stringfilter
def get_atr(form, form_name):
    return form[str(form_name)]