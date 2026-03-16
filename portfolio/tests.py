import shutil
import tempfile
from io import BytesIO
from pathlib import Path
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from unittest.mock import patch

from .models import BlogPost, ContactMessage, Project, SiteSettings


TEST_MEDIA_ROOT = Path(tempfile.gettempdir()) / 'my-web-test-media'


@override_settings(
    MEDIA_ROOT=TEST_MEDIA_ROOT,
    UPLOAD_IMAGE_MAX_WIDTH=0,
    UPLOAD_IMAGE_MAX_HEIGHT=0,
    UPLOAD_IMAGE_JPEG_QUALITY=80,
    UPLOAD_IMAGE_USE_TINYPNG=False,
)
class PortfolioSmokeTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpTestData(cls):
        settings = SiteSettings.objects.first() or SiteSettings()
        settings.site_name = 'Test Studio'
        settings.hero_highlight_name = 'Jane'
        settings.hero_name_suffix = 'Doe'
        settings.hero_role = 'Creative Developer'
        settings.hero_role_ru = 'Kreativniy razrabotchik'
        settings.about_title = 'Test about'
        settings.about_description = 'Test description'
        settings.office_address = 'Tashkent'
        settings.contact_email = 'hello@example.com'
        settings.contact_phone = '+998 90 000 00 00'
        settings.save()
        cls.project = Project.objects.create(
            title='Landing Page Refresh',
            category='Web Design',
            short_description='A modern redesign for a SaaS company.',
            description='Detailed project story.',
            image_path='assets/images/protfolio/img-1.jpg',
            client_name='Acme',
        )
        cls.post = BlogPost.objects.create(
            title='Design System Basics',
            author_name='Admin',
            summary='Why consistency matters in product design.',
            content='A longer article body.',
            image_path='assets/images/blog/1.jpg',
        )

    @staticmethod
    def build_uploaded_image(size=(1400, 900), color=(200, 80, 80)):
        buffer = BytesIO()
        image = Image.new('RGB', size, color)
        image.save(buffer, format='JPEG', quality=95)
        return buffer.getvalue()

    def test_home_page_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Creative Developer')
        self.assertContains(response, 'assets/images/site-logo.png')
        self.assertContains(response, '<link rel="canonical" href="http://testserver/">', html=True)
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, 'og:title')
        self.assertContains(response, 'assets/js/site.js')
        self.assertContains(response, 'loading="lazy"')
        self.assertNotContains(response, 'jquery-plugin-collection.js')
        self.assertNotContains(response, 'tw-elements.umd.min.js')
        self.assertNotContains(response, 'jquery.min.js')

    def test_uploaded_about_image_overrides_static_fallback(self):
        settings = SiteSettings.objects.first()
        uploaded_image = self.build_uploaded_image()
        settings.about_image_file = SimpleUploadedFile(
            'about-upload.jpg',
            uploaded_image,
            content_type='image/jpeg',
        )
        settings.save()

        with Image.open(settings.about_image_file.path) as saved_image:
            self.assertEqual(saved_image.width, 1400)
            self.assertEqual(saved_image.height, 900)
        self.assertLess(Path(settings.about_image_file.path).stat().st_size, len(uploaded_image))

        response = self.client.get(reverse('about'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/media/site/about-upload')

    def test_default_logo_path_is_updated(self):
        self.assertEqual(SiteSettings.objects.first().logo_image, 'assets/images/site-logo.png')
        self.assertEqual(SiteSettings.objects.first().footer_logo_image, 'assets/images/site-logo.png')

    def test_contact_form_creates_message(self):
        with patch('portfolio.views.send_contact_message_notification') as notify_mock:
            response = self.client.post(
                reverse('contact'),
                {
                    'first_name': 'Ali',
                    'last_name': 'Valiyev',
                    'email': 'ali@example.com',
                    'subject': 'New project',
                    'message': 'I want to discuss a landing page.',
                },
            )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().language_code, 'en')
        notify_mock.assert_called_once()

    def test_project_detail_renders(self):
        response = self.client.get(reverse('project_detail', args=[self.project.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Landing Page Refresh')

    def test_blog_detail_renders(self):
        response = self.client.get(reverse('blog_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Design System Basics')
        self.assertContains(response, 'article:published_time')
        self.assertContains(response, 'BlogPosting')

    def test_language_switch_changes_rendered_content(self):
        self.client.get(reverse('switch_language', args=['ru']), {'next': reverse('home')})
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kreativniy razrabotchik')

    def test_robots_txt_exposes_sitemap(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitemap: http://testserver/sitemap.xml')
        self.assertContains(response, 'Disallow: /admin/')

    def test_sitemap_includes_public_pages(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('home'))
        self.assertContains(response, reverse('project_detail', args=[self.project.slug]))
        self.assertContains(response, reverse('blog_detail', args=[self.post.slug]))

# Create your tests here.
