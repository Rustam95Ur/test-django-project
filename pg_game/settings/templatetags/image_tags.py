from django import template

register = template.Library()


@register.filter
def image_url_update(value):
    return value.replace("static", "media")
