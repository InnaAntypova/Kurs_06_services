from django import template

register = template.Library()


@register.filter
def my_media(value):
    if value:
        return f"/media/mail_sender/{value}"
    return ""
