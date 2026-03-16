from functools import lru_cache
from pathlib import Path

from django import template
from django.conf import settings

from PIL import Image

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


def _get_uploaded_asset_path(instance, field_name):
    file_field = getattr(instance, f'{field_name}_file', None)
    if not file_field:
        return None

    try:
        return Path(file_field.path)
    except (NotImplementedError, ValueError):
        return None


def _resolve_static_asset_path(asset_path):
    if not asset_path or asset_path.startswith(('http://', 'https://', '//')):
        return None

    relative_path = asset_path.lstrip('/')
    media_url = getattr(settings, 'MEDIA_URL', '').lstrip('/')
    if media_url and relative_path.startswith(media_url):
        media_candidate = Path(settings.MEDIA_ROOT) / relative_path[len(media_url):].lstrip('/')
        if media_candidate.exists():
            return media_candidate

    for static_dir in getattr(settings, 'STATICFILES_DIRS', []):
        candidate = Path(static_dir) / relative_path
        if candidate.exists():
            return candidate

    static_root = getattr(settings, 'STATIC_ROOT', None)
    if static_root:
        candidate = Path(static_root) / relative_path
        if candidate.exists():
            return candidate

    return None


@lru_cache(maxsize=256)
def _read_image_dimensions(path_string):
    try:
        with Image.open(path_string) as image:
            return {'width': image.width, 'height': image.height}
    except (FileNotFoundError, OSError, ValueError):
        return {'width': '', 'height': ''}


def _get_asset_dimensions(instance, field_name):
    if not instance:
        return {'width': '', 'height': ''}

    uploaded_asset_path = _get_uploaded_asset_path(instance, field_name)
    if uploaded_asset_path:
        return _read_image_dimensions(str(uploaded_asset_path))

    fallback_asset_path = getattr(instance, field_name, '')
    resolved_path = _resolve_static_asset_path(fallback_asset_path)
    if not resolved_path:
        return {'width': '', 'height': ''}

    return _read_image_dimensions(str(resolved_path))


@register.filter
def asset_width(instance, field_name):
    return _get_asset_dimensions(instance, field_name)['width']


@register.filter
def asset_height(instance, field_name):
    return _get_asset_dimensions(instance, field_name)['height']
