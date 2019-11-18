from django.template.library import Library
from jedzonko.models import Page
import re

register = Library()


@register.filter
def in_slugs(slug):
    if Page.objects.filter(slug=slug):
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def activeclass(context, slug):
    request = context['request']
    if re.match(r'^'+slug, request.META['PATH_INFO'].strip(' /')):
        return ' active'
    else:
        return ''

# do poczytania https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
