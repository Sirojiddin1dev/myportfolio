from django import template

from portfolio.translation_utils import translate_model_field

register = template.Library()


@register.filter
def tr(instance, field_name):
    return translate_model_field(instance, field_name)


@register.filter
def asset_url(instance, field_name):
    if not instance or not hasattr(instance, 'get_asset_url'):
        return ''
    return instance.get_asset_url(field_name)
