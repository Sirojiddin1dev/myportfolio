from django.utils import translation

from .translation_utils import normalize_language_code


class SiteLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language_code = normalize_language_code(
            request.session.get('site_language') or request.COOKIES.get('site_language')
        )
        request.current_language = language_code
        request.LANGUAGE_CODE = language_code
        translation.activate(language_code)
        response = self.get_response(request)
        response.set_cookie('site_language', language_code, max_age=60 * 60 * 24 * 365)
        return response
