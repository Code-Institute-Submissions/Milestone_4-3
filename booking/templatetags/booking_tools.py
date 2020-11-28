from django import template


register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, days):
    return price * days
