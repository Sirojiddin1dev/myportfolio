import json

from django.utils.html import strip_tags
from django.utils.text import Truncator

from .models import SiteSettings, SocialLink
from .translation_utils import get_current_language, get_ui_text, translate_model_field


LOCALE_BY_LANGUAGE = {
    'en': 'en_US',
    'ru': 'ru_RU',
    'uz': 'uz_UZ',
}


def _site_settings():
    return SiteSettings.objects.first() or SiteSettings()


def _social_urls():
    return list(SocialLink.objects.exclude(url='').values_list('url', flat=True))


def _clean_text(value, max_length=160):
    plain_text = ' '.join(strip_tags(value or '').split())
    return Truncator(plain_text).chars(max_length)


def _absolute_url(request, value):
    if not value:
        return ''
    if value.startswith(('http://', 'https://')):
        return value
    return request.build_absolute_uri(value)


def _person_name(site_settings, language_code):
    first_name = site_settings.get_translated('hero_highlight_name', language_code)
    last_name = site_settings.get_translated('hero_name_suffix', language_code)
    return ' '.join(part for part in [first_name, last_name] if part).strip() or site_settings.get_translated('site_name', language_code)


def _person_schema(request, site_settings, language_code):
    same_as = _social_urls()
    person = {
        '@context': 'https://schema.org',
        '@type': 'Person',
        'name': _person_name(site_settings, language_code),
        'jobTitle': site_settings.get_translated('hero_role', language_code),
        'url': request.build_absolute_uri('/'),
        'image': _absolute_url(request, site_settings.get_asset_url('about_image') or site_settings.get_asset_url('logo_image')),
        'email': site_settings.contact_email,
        'telephone': site_settings.contact_phone,
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': site_settings.get_translated('office_address', language_code),
        },
    }
    if same_as:
        person['sameAs'] = same_as
    return person


def _website_schema(request, site_settings, language_code):
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        'name': site_settings.get_translated('site_name', language_code),
        'url': request.build_absolute_uri('/'),
        'description': _clean_text(site_settings.get_translated('meta_description', language_code)),
        'inLanguage': language_code,
    }


def _page_schema(canonical_url, title, description, schema_type, language_code):
    return {
        '@context': 'https://schema.org',
        '@type': schema_type,
        'name': title,
        'url': canonical_url,
        'description': description,
        'inLanguage': language_code,
    }


def _serialize_schemas(schemas):
    return [json.dumps(schema, ensure_ascii=False) for schema in schemas if schema]


def build_seo_context(
    request,
    *,
    title,
    description,
    image=None,
    og_type='website',
    schema_type='WebPage',
    extra_schemas=None,
    published_time=None,
    modified_time=None,
    robots='index,follow',
):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    canonical_url = request.build_absolute_uri(request.path)
    resolved_image = image or site_settings.get_asset_url('about_image') or site_settings.get_asset_url('hero_background_image') or site_settings.get_asset_url('logo_image')
    absolute_image = _absolute_url(request, resolved_image)
    site_name = site_settings.get_translated('site_name', current_language)
    meta_description = _clean_text(description or site_settings.get_translated('meta_description', current_language))

    schemas = [
        _website_schema(request, site_settings, current_language),
        _person_schema(request, site_settings, current_language),
        _page_schema(canonical_url, title, meta_description, schema_type, current_language),
    ]
    schemas.extend(extra_schemas or [])

    return {
        'title': title,
        'description': meta_description,
        'canonical_url': canonical_url,
        'robots': robots,
        'site_name': site_name,
        'image': absolute_image,
        'image_alt': title,
        'og_type': og_type,
        'locale': LOCALE_BY_LANGUAGE.get(current_language, 'en_US'),
        'alternate_locales': [
            locale for code, locale in LOCALE_BY_LANGUAGE.items() if code != current_language
        ],
        'twitter_card': 'summary_large_image' if absolute_image else 'summary',
        'published_time': published_time.isoformat() if published_time else '',
        'modified_time': modified_time.isoformat() if modified_time else '',
        'author': _person_name(site_settings, current_language),
        'schemas': _serialize_schemas(schemas),
    }


def build_home_seo(request):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    person_name = _person_name(site_settings, current_language)
    role = site_settings.get_translated('hero_role', current_language)
    title = f'{person_name} | {role}'
    description = site_settings.get_translated('meta_description', current_language)
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=site_settings.get_asset_url('hero_background_image'),
        og_type='website',
        schema_type='WebPage',
    )


def build_about_seo(request):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{get_ui_text('about', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = site_settings.get_translated('about_description', current_language)
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=site_settings.get_asset_url('about_image'),
        og_type='profile',
        schema_type='AboutPage',
    )


def build_portfolio_list_seo(request):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{get_ui_text('portfolio', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = get_ui_text('selected_client_work_and_case_studies', current_language)
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=site_settings.get_asset_url('about_image'),
        og_type='website',
        schema_type='CollectionPage',
    )


def build_project_seo(request, project):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{translate_model_field(project, 'title', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = translate_model_field(project, 'short_description', current_language) or translate_model_field(project, 'description', current_language)
    creative_work_schema = {
        '@context': 'https://schema.org',
        '@type': 'CreativeWork',
        'name': translate_model_field(project, 'title', current_language),
        'description': _clean_text(description),
        'url': request.build_absolute_uri(request.path),
        'image': _absolute_url(request, project.get_asset_url('image_path')),
        'dateCreated': project.created_at.isoformat(),
        'dateModified': project.updated_at.isoformat(),
        'genre': translate_model_field(project, 'category', current_language),
        'creator': {
            '@type': 'Person',
            'name': _person_name(site_settings, current_language),
        },
    }
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=project.get_asset_url('image_path'),
        og_type='article',
        schema_type='WebPage',
        extra_schemas=[creative_work_schema],
        modified_time=project.updated_at,
    )


def build_blog_list_seo(request):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{get_ui_text('blog', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = get_ui_text('latest_notes_ideas_and_updates', current_language)
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=site_settings.get_asset_url('hero_background_image'),
        og_type='website',
        schema_type='CollectionPage',
    )


def build_blog_post_seo(request, post):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{translate_model_field(post, 'title', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = translate_model_field(post, 'summary', current_language) or translate_model_field(post, 'content', current_language)
    blog_schema = {
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        'headline': translate_model_field(post, 'title', current_language),
        'description': _clean_text(description),
        'image': _absolute_url(request, post.get_asset_url('image_path')),
        'datePublished': post.published_at.isoformat(),
        'dateModified': post.updated_at.isoformat(),
        'author': {
            '@type': 'Person',
            'name': translate_model_field(post, 'author_name', current_language),
        },
        'publisher': {
            '@type': 'Person',
            'name': _person_name(site_settings, current_language),
        },
        'mainEntityOfPage': request.build_absolute_uri(request.path),
        'url': request.build_absolute_uri(request.path),
    }
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=post.get_asset_url('image_path'),
        og_type='article',
        schema_type='Article',
        extra_schemas=[blog_schema],
        published_time=post.published_at,
        modified_time=post.updated_at,
    )


def build_contact_seo(request):
    current_language = get_current_language(request)
    site_settings = _site_settings()
    title = f"{get_ui_text('contact', current_language)} | {site_settings.get_translated('site_name', current_language)}"
    description = get_ui_text('start_conversation_about_your_next_project', current_language)
    return build_seo_context(
        request,
        title=title,
        description=description,
        image=site_settings.get_asset_url('about_image'),
        og_type='website',
        schema_type='ContactPage',
    )
