from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost, Project, SiteSettings


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['home', 'about', 'portfolio', 'blog_list', 'contact']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return (SiteSettings.objects.first() or SiteSettings()).updated_at


class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Project.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('project_detail', args=[obj.slug])


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])
