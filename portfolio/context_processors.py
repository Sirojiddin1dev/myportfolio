from .models import SiteSettings, SocialLink
from .translation_utils import LANGUAGE_CHOICES, get_current_language, get_ui_bundle


def site_context(request):
    current_language = get_current_language(request)
    return {
        'site_settings': SiteSettings.objects.first() or SiteSettings(),
        'social_links': SocialLink.objects.all(),
        'current_language': current_language,
        'available_languages': LANGUAGE_CHOICES,
        'ui_text': get_ui_bundle(current_language),
        'current_absolute_url': request.build_absolute_uri(request.path),
    }
