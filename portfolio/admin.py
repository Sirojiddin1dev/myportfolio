from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Award,
    BlogPost,
    ContactMessage,
    Project,
    Service,
    SiteSettings,
    Skill,
    SocialLink,
    Testimonial,
)


class UploadedAssetPreviewAdminMixin:
    asset_field_name = None

    @admin.display(description='Preview')
    def image_preview(self, obj):
        if not obj or not obj.pk:
            return 'Save to preview the image.'

        image_url = obj.get_asset_url(self.asset_field_name)
        if not image_url:
            return 'No image selected.'

        return format_html(
            '<img src="{}" alt="" style="max-height: 120px; border-radius: 8px; object-fit: cover;" />',
            image_url,
        )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'hero_role', 'contact_email', 'contact_phone', 'updated_at')
    fieldsets = (
        (
            'Branding',
            {
                'fields': (
                    'site_name',
                    'site_name_ru',
                    'site_name_uz',
                    'brand_name',
                    'brand_name_ru',
                    'brand_name_uz',
                    'meta_description',
                    'meta_description_ru',
                    'meta_description_uz',
                    'logo_image_file',
                    'logo_image',
                    'footer_logo_image_file',
                    'footer_logo_image',
                    'favicon_image_file',
                    'favicon_image',
                )
            },
        ),
        (
            'Hero section',
            {
                'fields': (
                    'hero_pre_title',
                    'hero_pre_title_ru',
                    'hero_pre_title_uz',
                    'hero_highlight_name',
                    'hero_highlight_name_ru',
                    'hero_highlight_name_uz',
                    'hero_name_suffix',
                    'hero_name_suffix_ru',
                    'hero_name_suffix_uz',
                    'hero_role',
                    'hero_role_ru',
                    'hero_role_uz',
                    'hero_background_image_file',
                    'hero_background_image',
                    'hero_shape_image_file',
                    'hero_shape_image',
                )
            },
        ),
        (
            'About and contact',
            {
                'fields': (
                    'about_title',
                    'about_title_ru',
                    'about_title_uz',
                    'about_description',
                    'about_description_ru',
                    'about_description_uz',
                    'about_image_file',
                    'about_image',
                    'experience_years',
                    'office_address',
                    'office_address_ru',
                    'office_address_uz',
                    'contact_email',
                    'contact_phone',
                    'call_to_action_text',
                    'call_to_action_text_ru',
                    'call_to_action_text_uz',
                    'copyright_text',
                    'copyright_text_ru',
                    'copyright_text_uz',
                )
            },
        ),
    )


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'accent_color', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'name_ru', 'name_uz', 'url', 'icon_class', 'hero_icon_class')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'accent_color', 'order')
    list_editable = ('percentage', 'order')
    search_fields = ('name', 'name_ru', 'name_uz')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'updated_at')
    list_editable = ('order',)
    search_fields = ('title', 'title_ru', 'title_uz', 'description', 'description_ru', 'description_uz', 'icon_class')


@admin.register(Award)
class AwardAdmin(UploadedAssetPreviewAdminMixin, admin.ModelAdmin):
    asset_field_name = 'image_path'
    list_display = ('title', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_preview',)
    fields = ('title', 'title_ru', 'title_uz', 'order', 'image_preview', 'image_path_file', 'image_path')
    search_fields = ('title', 'title_ru', 'title_uz')


@admin.register(Project)
class ProjectAdmin(UploadedAssetPreviewAdminMixin, admin.ModelAdmin):
    asset_field_name = 'image_path'
    list_display = ('title', 'category', 'client_name', 'is_featured', 'order')
    list_filter = ('is_featured', 'category')
    list_editable = ('is_featured', 'order')
    readonly_fields = ('image_preview',)
    fields = (
        'title',
        'title_ru',
        'title_uz',
        'slug',
        'category',
        'category_ru',
        'category_uz',
        'short_description',
        'short_description_ru',
        'short_description_uz',
        'description',
        'description_ru',
        'description_uz',
        'client_name',
        'client_name_ru',
        'client_name_uz',
        'project_url',
        'is_featured',
        'order',
        'image_preview',
        'image_path_file',
        'image_path',
    )
    search_fields = (
        'title',
        'title_ru',
        'title_uz',
        'category',
        'category_ru',
        'category_uz',
        'client_name',
        'client_name_ru',
        'client_name_uz',
        'short_description',
        'short_description_ru',
        'short_description_uz',
        'description',
        'description_ru',
        'description_uz',
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(UploadedAssetPreviewAdminMixin, admin.ModelAdmin):
    asset_field_name = 'image_path'
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)
    readonly_fields = ('image_preview',)
    fields = (
        'name',
        'name_ru',
        'name_uz',
        'role',
        'role_ru',
        'role_uz',
        'quote',
        'quote_ru',
        'quote_uz',
        'order',
        'image_preview',
        'image_path_file',
        'image_path',
    )
    search_fields = ('name', 'name_ru', 'name_uz', 'role', 'role_ru', 'role_uz', 'quote', 'quote_ru', 'quote_uz')


@admin.register(BlogPost)
class BlogPostAdmin(UploadedAssetPreviewAdminMixin, admin.ModelAdmin):
    asset_field_name = 'image_path'
    list_display = ('title', 'author_name', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    list_editable = ('is_published',)
    readonly_fields = ('image_preview',)
    fields = (
        'title',
        'title_ru',
        'title_uz',
        'slug',
        'author_name',
        'author_name_ru',
        'author_name_uz',
        'summary',
        'summary_ru',
        'summary_uz',
        'content',
        'content_ru',
        'content_uz',
        'published_at',
        'is_published',
        'image_preview',
        'image_path_file',
        'image_path',
    )
    search_fields = (
        'title',
        'title_ru',
        'title_uz',
        'summary',
        'summary_ru',
        'summary_uz',
        'content',
        'content_ru',
        'content_uz',
        'author_name',
        'author_name_ru',
        'author_name_uz',
    )
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'language_code', 'subject', 'is_read', 'created_at')
    list_filter = ('language_code', 'is_read', 'created_at')
    list_editable = ('is_read',)
    readonly_fields = ('first_name', 'last_name', 'email', 'language_code', 'subject', 'message', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject', 'message')


admin.site.site_header = 'Follio Admin'
admin.site.site_title = 'Follio Admin'
admin.site.index_title = 'Portfolio content management'

# Register your models here.
