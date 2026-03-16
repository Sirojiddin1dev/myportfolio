from datetime import date

from django.db import migrations


def seed_demo_content(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    SocialLink = apps.get_model('portfolio', 'SocialLink')
    Skill = apps.get_model('portfolio', 'Skill')
    Service = apps.get_model('portfolio', 'Service')
    Award = apps.get_model('portfolio', 'Award')
    Project = apps.get_model('portfolio', 'Project')
    Testimonial = apps.get_model('portfolio', 'Testimonial')
    BlogPost = apps.get_model('portfolio', 'BlogPost')

    if not SiteSettings.objects.exists():
        SiteSettings.objects.create(
            site_name='Follio Studio',
            brand_name='Follio',
            meta_description='A Bootstrap portfolio template converted into a Django site with admin-managed content.',
            hero_pre_title="I'm",
            hero_highlight_name='John',
            hero_name_suffix='Smith',
            hero_role='Freelance UI/UX Designer',
            about_title='I create products, not just art',
            about_description=(
                'This portfolio template has been connected to Django admin. '
                'You can now edit hero text, services, skills, portfolio cards, '
                'testimonials, and blog posts directly from the admin dashboard.'
            ),
            experience_years=7,
            office_address='25 North Street, Tashkent',
            contact_email='info@folliostudio.com',
            contact_phone='+998 90 123 45 67',
            call_to_action_text="Let's Talk",
            copyright_text='2026 Follio. All rights reserved.',
            logo_image='assets/images/site-logo.png',
            footer_logo_image='assets/images/site-logo.png',
            favicon_image='assets/images/favicon.png',
            hero_background_image='assets/images/slider/slide-1.jpg',
            hero_shape_image='assets/images/slider/hero-shape.png',
            about_image='assets/images/about/about.png',
        )

    if not SocialLink.objects.exists():
        SocialLink.objects.bulk_create(
            [
                SocialLink(
                    name='Dribbble',
                    url='https://dribbble.com/',
                    icon_class='fa fa-dribbble',
                    hero_icon_class='ti-dribbble',
                    accent_color='#ea4c89',
                    order=1,
                ),
                SocialLink(
                    name='LinkedIn',
                    url='https://linkedin.com/',
                    icon_class='fa fa-linkedin',
                    hero_icon_class='ti-linkedin',
                    accent_color='#0077b5',
                    order=2,
                ),
                SocialLink(
                    name='Instagram',
                    url='https://instagram.com/',
                    icon_class='fa fa-instagram',
                    hero_icon_class='ti-instagram',
                    accent_color='#ff8e40',
                    order=3,
                ),
                SocialLink(
                    name='Twitter',
                    url='https://x.com/',
                    icon_class='fa fa-twitter',
                    hero_icon_class='ti-twitter',
                    accent_color='#03a9f4',
                    order=4,
                ),
                SocialLink(
                    name='Behance',
                    url='https://behance.net/',
                    icon_class='fa fa-behance',
                    hero_icon_class='ti-palette',
                    accent_color='#4176fa',
                    order=5,
                ),
            ]
        )

    if not Skill.objects.exists():
        Skill.objects.bulk_create(
            [
                Skill(name='Communication Skills', percentage=75, accent_color='#fe3e57', order=1),
                Skill(name='Project Management', percentage=90, accent_color='#54faae', order=2),
                Skill(name='Problem Solving', percentage=65, accent_color='#ff8c2f', order=3),
                Skill(name='Analytical Thinking', percentage=55, accent_color='#f1f965', order=4),
                Skill(name='Organization', percentage=40, accent_color='#ff0173', order=5),
                Skill(name='Creativity', percentage=85, accent_color='#39c4ff', order=6),
            ]
        )

    if not Service.objects.exists():
        Service.objects.bulk_create(
            [
                Service(
                    title='Product Design',
                    description='User-focused product strategy, wireframes, and polished interface systems.',
                    icon_class='fi flaticon-idea',
                    background_shape_path='assets/images/wpo-service/shape.png',
                    order=1,
                ),
                Service(
                    title='Web Design',
                    description='Responsive website design that keeps brand, usability, and performance aligned.',
                    icon_class='fi flaticon-files-and-folders',
                    background_shape_path='assets/images/wpo-service/shape-2.png',
                    order=2,
                ),
                Service(
                    title='Visual Design',
                    description='Strong visual direction for campaigns, landing pages, and portfolio experiences.',
                    icon_class='fi flaticon-artist',
                    background_shape_path='assets/images/wpo-service/shape-3.png',
                    order=3,
                ),
                Service(
                    title='Business Strategy',
                    description='Creative consulting that connects customer needs with measurable product outcomes.',
                    icon_class='fi flaticon-man',
                    background_shape_path='assets/images/wpo-service/shape-4.png',
                    order=4,
                ),
            ]
        )

    if not Award.objects.exists():
        Award.objects.bulk_create(
            [
                Award(title='Award One', image_path='assets/images/about/award.jpg', order=1),
                Award(title='Award Two', image_path='assets/images/about/award2.jpg', order=2),
                Award(title='Award Three', image_path='assets/images/about/award3.jpg', order=3),
                Award(title='Award Four', image_path='assets/images/about/award4.jpg', order=4),
            ]
        )

    if not Project.objects.exists():
        Project.objects.bulk_create(
            [
                Project(
                    title='Minimalism',
                    slug='minimalism',
                    category='Illustration . Art Direction',
                    short_description='A clean visual identity project with bold editorial direction.',
                    description='Minimalism is a branding and showcase project focused on clarity, whitespace, and confident typography.',
                    image_path='assets/images/protfolio/img-1.jpg',
                    client_name='North Studio',
                    project_url='https://example.com/minimalism',
                    is_featured=True,
                    order=1,
                ),
                Project(
                    title='3D Project',
                    slug='3d-project',
                    category='Illustration . Art Direction',
                    short_description='A concept-heavy visual exploration built with immersive presentation layers.',
                    description='This project combines visual storytelling, 3D mockups, and polished motion-friendly layouts.',
                    image_path='assets/images/protfolio/img-2.jpg',
                    client_name='Vertex Labs',
                    project_url='https://example.com/3d-project',
                    is_featured=True,
                    order=2,
                ),
                Project(
                    title='Abstract Art',
                    slug='abstract-art',
                    category='Illustration . Art Direction',
                    short_description='A textured campaign look blending modern art references with digital interactions.',
                    description='Abstract Art turns a gallery-inspired concept into an engaging product marketing experience.',
                    image_path='assets/images/protfolio/img-3.jpg',
                    client_name='Muse Creative',
                    project_url='https://example.com/abstract-art',
                    is_featured=True,
                    order=3,
                ),
                Project(
                    title='Modern BG',
                    slug='modern-bg',
                    category='Illustration . Art Direction',
                    short_description='A visual system with atmospheric backgrounds and bold presentation blocks.',
                    description='Modern BG focuses on striking contrast, modular content areas, and a premium visual tone.',
                    image_path='assets/images/protfolio/img-4.jpg',
                    client_name='Frame Works',
                    project_url='https://example.com/modern-bg',
                    is_featured=True,
                    order=4,
                ),
            ]
        )

    if not Testimonial.objects.exists():
        Testimonial.objects.bulk_create(
            [
                Testimonial(
                    name='John Harry',
                    role='CEO of Moderntern',
                    quote='The admin workflow is clean and the template now feels like a real product site, not just static HTML.',
                    image_path='assets/images/testimonials/img-1.jpg',
                    order=1,
                ),
                Testimonial(
                    name='Amelia Stone',
                    role='Founder of Studio North',
                    quote='Fast delivery, thoughtful structure, and a frontend that still preserves the original design energy.',
                    image_path='assets/images/testimonials/img-4.jpg',
                    order=2,
                ),
                Testimonial(
                    name='Daniel Cruz',
                    role='Product Lead at Vertex Labs',
                    quote='Being able to edit the homepage content and portfolio cards from Django admin made handoff much easier.',
                    image_path='assets/images/testimonials/img-3.jpg',
                    order=3,
                ),
            ]
        )

    if not BlogPost.objects.exists():
        BlogPost.objects.bulk_create(
            [
                BlogPost(
                    title='Helpful tips for becoming a successful designer',
                    slug='helpful-tips-for-becoming-a-successful-designer',
                    author_name='Admin',
                    summary='Practical habits that help creative work stay consistent, sharp, and client-ready.',
                    content=(
                        'Strong design comes from repetition, critique, and curiosity.\n\n'
                        'Build systems, not one-off screens. Keep your files clean. Learn to explain why a decision helps the user.\n\n'
                        'The biggest jump often comes from turning good visual taste into repeatable process.'
                    ),
                    image_path='assets/images/blog/1.jpg',
                    published_at=date(2026, 3, 1),
                    is_published=True,
                ),
                BlogPost(
                    title='Why structured admin content saves time later',
                    slug='why-structured-admin-content-saves-time-later',
                    author_name='Admin',
                    summary='Turning template text into models pays off when clients want updates without code edits.',
                    content=(
                        'A static template is fast to preview, but admin-driven content is what makes it sustainable.\n\n'
                        'Once projects, services, and testimonials live in the database, updates become safer and much quicker.'
                    ),
                    image_path='assets/images/blog/2.jpg',
                    published_at=date(2026, 3, 5),
                    is_published=True,
                ),
                BlogPost(
                    title='From Bootstrap template to Django website',
                    slug='from-bootstrap-template-to-django-website',
                    author_name='Admin',
                    summary='A short breakdown of what changes when a static theme becomes a working web app.',
                    content=(
                        'The main shift is not visual, it is structural.\n\n'
                        'Views, URLs, templates, models, and admin turn a design asset into something a team can actually manage over time.'
                    ),
                    image_path='assets/images/blog/3.jpg',
                    published_at=date(2026, 3, 8),
                    is_published=True,
                ),
            ]
        )


def unseed_demo_content(apps, schema_editor):
    models_to_clear = [
        apps.get_model('portfolio', 'BlogPost'),
        apps.get_model('portfolio', 'Testimonial'),
        apps.get_model('portfolio', 'Project'),
        apps.get_model('portfolio', 'Award'),
        apps.get_model('portfolio', 'Service'),
        apps.get_model('portfolio', 'Skill'),
        apps.get_model('portfolio', 'SocialLink'),
        apps.get_model('portfolio', 'SiteSettings'),
    ]
    for model in models_to_clear:
        model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_content, unseed_demo_content),
    ]
