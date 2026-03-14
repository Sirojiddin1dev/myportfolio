import logging

from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils import timezone
from django.utils.text import slugify

from .translation_utils import DEFAULT_LANGUAGE, LANGUAGE_CHOICES, normalize_language_code


logger = logging.getLogger(__name__)


def build_unique_slug(instance, source_value, slug_field_name='slug'):
    base_slug = slugify(source_value) or 'item'
    slug = base_slug
    model_class = instance.__class__
    counter = 2
    while model_class.objects.exclude(pk=instance.pk).filter(**{slug_field_name: slug}).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


class AssetFallbackMixin:
    def get_asset_url(self, field_name):
        uploaded_asset = getattr(self, f'{field_name}_file', None)
        if uploaded_asset:
            try:
                return uploaded_asset.url
            except ValueError:
                pass

        fallback_path = getattr(self, field_name, '')
        if not fallback_path:
            return ''
        if fallback_path.startswith(('http://', 'https://', '/')):
            return fallback_path
        return static(fallback_path)


class UploadedImageOptimizationMixin(models.Model):
    class Meta:
        abstract = True

    def _pending_uploaded_file_field_names(self):
        pending_fields = []
        for field in self._meta.fields:
            if not isinstance(field, models.FileField):
                continue
            field_file = getattr(self, field.name, None)
            if field_file and not field_file._committed:
                pending_fields.append(field.name)
        return pending_fields

    def _optimize_uploaded_images(self, field_names):
        if not field_names:
            return

        try:
            from image_compressor import compress_uploaded_image
        except Exception as exc:  # pragma: no cover - import environment issue
            logger.warning('Image compressor could not be imported: %s', exc)
            return

        for field_name in field_names:
            field_file = getattr(self, field_name, None)
            if not field_file:
                continue
            result = compress_uploaded_image(
                field_file,
                jpeg_quality=getattr(settings, 'UPLOAD_IMAGE_JPEG_QUALITY', 85),
                max_width=getattr(settings, 'UPLOAD_IMAGE_MAX_WIDTH', 1600),
                max_height=getattr(settings, 'UPLOAD_IMAGE_MAX_HEIGHT', 1600),
                use_tinypng=getattr(settings, 'UPLOAD_IMAGE_USE_TINYPNG', False),
            )
            if not result.get('success'):
                logger.warning(
                    'Uploaded image optimization failed for %s.%s: %s',
                    self.__class__.__name__,
                    field_name,
                    result.get('message'),
                )

    def save(self, *args, **kwargs):
        pending_fields = self._pending_uploaded_file_field_names()
        super().save(*args, **kwargs)
        self._optimize_uploaded_images(pending_fields)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    def get_translated(self, field_name, language_code=None):
        normalized_language = normalize_language_code(language_code)
        if normalized_language != DEFAULT_LANGUAGE:
            translated_value = getattr(self, f'{field_name}_{normalized_language}', '')
            if translated_value:
                return translated_value
        return getattr(self, field_name, '')


class SiteSettings(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    site_name = models.CharField(max_length=120, default='Follio Studio')
    site_name_ru = models.CharField(max_length=120, blank=True)
    site_name_uz = models.CharField(max_length=120, blank=True)
    brand_name = models.CharField(max_length=80, default='Follio')
    brand_name_ru = models.CharField(max_length=80, blank=True)
    brand_name_uz = models.CharField(max_length=80, blank=True)
    meta_description = models.CharField(
        max_length=160,
        default='Creative portfolio site powered by Django.',
    )
    meta_description_ru = models.CharField(max_length=160, blank=True)
    meta_description_uz = models.CharField(max_length=160, blank=True)
    hero_pre_title = models.CharField(max_length=30, default="I'm")
    hero_pre_title_ru = models.CharField(max_length=30, blank=True)
    hero_pre_title_uz = models.CharField(max_length=30, blank=True)
    hero_highlight_name = models.CharField(max_length=40, default='John')
    hero_highlight_name_ru = models.CharField(max_length=40, blank=True)
    hero_highlight_name_uz = models.CharField(max_length=40, blank=True)
    hero_name_suffix = models.CharField(max_length=40, default='Smith')
    hero_name_suffix_ru = models.CharField(max_length=40, blank=True)
    hero_name_suffix_uz = models.CharField(max_length=40, blank=True)
    hero_role = models.CharField(max_length=120, default='Freelance UI/UX Designer')
    hero_role_ru = models.CharField(max_length=120, blank=True)
    hero_role_uz = models.CharField(max_length=120, blank=True)
    about_title = models.CharField(max_length=160, default='I create products, not just art')
    about_title_ru = models.CharField(max_length=160, blank=True)
    about_title_uz = models.CharField(max_length=160, blank=True)
    about_description = models.TextField(
        default=(
            'I design memorable digital experiences for ambitious brands. '
            'This portfolio is fully editable from Django admin, so text, '
            'projects, and testimonials can all be updated without touching code.'
        )
    )
    about_description_ru = models.TextField(blank=True)
    about_description_uz = models.TextField(blank=True)
    experience_years = models.PositiveSmallIntegerField(default=7)
    office_address = models.CharField(max_length=255, default='25 North Street, Tashkent')
    office_address_ru = models.CharField(max_length=255, blank=True)
    office_address_uz = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(default='info@example.com')
    contact_phone = models.CharField(max_length=40, default='+998 90 123 45 67')
    call_to_action_text = models.CharField(max_length=80, default="Let's Talk")
    call_to_action_text_ru = models.CharField(max_length=80, blank=True)
    call_to_action_text_uz = models.CharField(max_length=80, blank=True)
    copyright_text = models.CharField(max_length=120, default='2026 Follio. All rights reserved.')
    copyright_text_ru = models.CharField(max_length=120, blank=True)
    copyright_text_uz = models.CharField(max_length=120, blank=True)
    logo_image = models.CharField(max_length=255, default='assets/images/site-logo.png')
    logo_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    footer_logo_image = models.CharField(max_length=255, default='assets/images/site-logo.png')
    footer_logo_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    favicon_image = models.CharField(max_length=255, default='assets/images/favicon.png')
    favicon_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    hero_background_image = models.CharField(
        max_length=255,
        default='assets/images/slider/slide-1.jpg',
        help_text='Static asset path inside the bundled template.',
    )
    hero_background_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    hero_shape_image = models.CharField(
        max_length=255,
        default='assets/images/slider/hero-shape.png',
        help_text='Static asset path inside the bundled template.',
    )
    hero_shape_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    about_image = models.CharField(
        max_length=255,
        default='assets/images/about/about.png',
        help_text='Static asset path inside the bundled template.',
    )
    about_image_file = models.FileField(
        upload_to='site/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )

    class Meta:
        verbose_name = 'Site settings'
        verbose_name_plural = 'Site settings'

    def __str__(self):
        return self.site_name


class SocialLink(TimeStampedModel, TranslatableModel):
    name = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50, blank=True)
    name_uz = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    icon_class = models.CharField(max_length=80, default='fa fa-link')
    hero_icon_class = models.CharField(max_length=80, blank=True)
    accent_color = models.CharField(max_length=20, default='#fe3e57')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Skill(TimeStampedModel, TranslatableModel):
    name = models.CharField(max_length=80)
    name_ru = models.CharField(max_length=80, blank=True)
    name_uz = models.CharField(max_length=80, blank=True)
    percentage = models.PositiveSmallIntegerField(default=75)
    accent_color = models.CharField(max_length=20, default='#fe3e57')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} ({self.percentage}%)'


class Service(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    title = models.CharField(max_length=120)
    title_ru = models.CharField(max_length=120, blank=True)
    title_uz = models.CharField(max_length=120, blank=True)
    description = models.TextField()
    description_ru = models.TextField(blank=True)
    description_uz = models.TextField(blank=True)
    icon_class = models.CharField(max_length=120, default='fi flaticon-idea')
    background_shape_path = models.CharField(
        max_length=255,
        default='assets/images/wpo-service/shape.png',
        help_text='Static asset path inside the bundled template.',
    )
    background_shape_path_file = models.FileField(
        upload_to='services/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Award(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    title = models.CharField(max_length=120)
    title_ru = models.CharField(max_length=120, blank=True)
    title_uz = models.CharField(max_length=120, blank=True)
    image_path = models.CharField(
        max_length=255,
        help_text='Static asset path inside the bundled template.',
    )
    image_path_file = models.FileField(
        upload_to='awards/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Project(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    title = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150, blank=True)
    title_uz = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.CharField(max_length=120)
    category_ru = models.CharField(max_length=120, blank=True)
    category_uz = models.CharField(max_length=120, blank=True)
    short_description = models.CharField(max_length=255)
    short_description_ru = models.CharField(max_length=255, blank=True)
    short_description_uz = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    description_ru = models.TextField(blank=True)
    description_uz = models.TextField(blank=True)
    image_path = models.CharField(
        max_length=255,
        help_text='Static asset path inside the bundled template.',
    )
    image_path_file = models.FileField(
        upload_to='projects/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    client_name = models.CharField(max_length=120, blank=True)
    client_name_ru = models.CharField(max_length=120, blank=True)
    client_name_uz = models.CharField(max_length=120, blank=True)
    project_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120, blank=True)
    name_uz = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=150)
    role_ru = models.CharField(max_length=150, blank=True)
    role_uz = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    quote_ru = models.TextField(blank=True)
    quote_uz = models.TextField(blank=True)
    image_path = models.CharField(
        max_length=255,
        help_text='Static asset path inside the bundled template.',
    )
    image_path_file = models.FileField(
        upload_to='testimonials/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class BlogPost(UploadedImageOptimizationMixin, AssetFallbackMixin, TimeStampedModel, TranslatableModel):
    title = models.CharField(max_length=160)
    title_ru = models.CharField(max_length=160, blank=True)
    title_uz = models.CharField(max_length=160, blank=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    author_name = models.CharField(max_length=80, default='Admin')
    author_name_ru = models.CharField(max_length=80, blank=True)
    author_name_uz = models.CharField(max_length=80, blank=True)
    summary = models.CharField(max_length=255)
    summary_ru = models.CharField(max_length=255, blank=True)
    summary_uz = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    content_ru = models.TextField(blank=True)
    content_uz = models.TextField(blank=True)
    image_path = models.CharField(
        max_length=255,
        help_text='Static asset path inside the bundled template.',
    )
    image_path_file = models.FileField(
        upload_to='blog/',
        blank=True,
        help_text='Optional uploaded image. If empty, the static path above is used.',
    )
    published_at = models.DateField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = build_unique_slug(self, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactMessage(TimeStampedModel):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    language_code = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email
