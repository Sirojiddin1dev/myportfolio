from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import ContactMessageForm
from .models import Award, BlogPost, Project, Service, Skill, Testimonial
from .seo import (
    build_about_seo,
    build_blog_list_seo,
    build_blog_post_seo,
    build_contact_seo,
    build_home_seo,
    build_portfolio_list_seo,
    build_project_seo,
)
from .telegram import send_contact_message_notification
from .translation_utils import get_current_language, get_ui_text, normalize_language_code


def build_contact_form(request, redirect_name):
    current_language = get_current_language(request)
    form = ContactMessageForm(request.POST or None, language_code=current_language)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.language_code = current_language
        message.save()
        send_contact_message_notification(message)
        messages.success(request, get_ui_text('contact_success', current_language))
        return redirect(redirect_name)
    return form


def home(request):
    contact_result = build_contact_form(request, 'home')
    if hasattr(contact_result, 'status_code'):
        return contact_result
    context = {
        'active_page': 'home',
        'skills': Skill.objects.all(),
        'services': Service.objects.all(),
        'awards': Award.objects.all(),
        'featured_projects': Project.objects.filter(is_featured=True)[:4],
        'testimonials': Testimonial.objects.all(),
        'latest_posts': BlogPost.objects.filter(is_published=True)[:3],
        'contact_form': contact_result,
        'seo': build_home_seo(request),
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    context = {
        'active_page': 'about',
        'skills': Skill.objects.all(),
        'services': Service.objects.all(),
        'awards': Award.objects.all(),
        'testimonials': Testimonial.objects.all(),
        'seo': build_about_seo(request),
    }
    return render(request, 'portfolio/about.html', context)


def portfolio_list(request):
    context = {
        'active_page': 'portfolio',
        'projects': Project.objects.all(),
        'seo': build_portfolio_list_seo(request),
    }
    return render(request, 'portfolio/portfolio_list.html', context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'active_page': 'portfolio',
        'project': project,
        'related_projects': Project.objects.exclude(pk=project.pk)[:3],
        'seo': build_project_seo(request, project),
    }
    return render(request, 'portfolio/project_detail.html', context)


def blog_list(request):
    context = {
        'active_page': 'blog',
        'posts': BlogPost.objects.filter(is_published=True),
        'seo': build_blog_list_seo(request),
    }
    return render(request, 'portfolio/blog_list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    context = {
        'active_page': 'blog',
        'post': post,
        'related_posts': BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:3],
        'seo': build_blog_post_seo(request, post),
    }
    return render(request, 'portfolio/blog_detail.html', context)


def contact(request):
    contact_result = build_contact_form(request, 'contact')
    if hasattr(contact_result, 'status_code'):
        return contact_result
    context = {
        'active_page': 'contact',
        'contact_form': contact_result,
        'seo': build_contact_seo(request),
    }
    return render(request, 'portfolio/contact.html', context)


def switch_language(request, language_code):
    language_code = normalize_language_code(language_code)
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('home')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = reverse('home')
    request.session['site_language'] = language_code
    response = redirect(next_url)
    response.set_cookie('site_language', language_code, max_age=60 * 60 * 24 * 365)
    return response


def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse('sitemap'))
    site_root = request.build_absolute_uri('/')
    content = '\n'.join(
        [
            'User-agent: *',
            'Allow: /',
            'Disallow: /admin/',
            'Disallow: /language/',
            f'Sitemap: {sitemap_url}',
            f'Host: {site_root.rstrip("/")}',
        ]
    )
    return HttpResponse(content, content_type='text/plain; charset=utf-8')
