from django.template.library import Library
from jedzonko.models import Page


register = Library()


@register.filter
def in_slugs(slug):
    if Page.objects.filter(slug=slug):
        return True
    else:
        return False

# do poczytania https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
