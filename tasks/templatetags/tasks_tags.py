from django import template

register = template.Library()


@register.inclusion_tag('tasks/_stars.html')
def show_stars(count):
    return {
        'star_count': range(count),
        'leftover_count': range(count, 5)
    }