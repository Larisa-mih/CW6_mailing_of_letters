from django import template

register = template.Library()


@register.filter
def is_content_manager(user):
    return user.groups.filter(name='content manager').exists()