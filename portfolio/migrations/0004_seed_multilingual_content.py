from django.db import migrations


def copy_translation_fields(instance, field_names):
    updated_fields = []
    for field_name in field_names:
        base_value = getattr(instance, field_name, '')
        ru_field = f'{field_name}_ru'
        uz_field = f'{field_name}_uz'
        if hasattr(instance, ru_field) and not getattr(instance, ru_field):
            setattr(instance, ru_field, base_value)
            updated_fields.append(ru_field)
        if hasattr(instance, uz_field) and not getattr(instance, uz_field):
            setattr(instance, uz_field, base_value)
            updated_fields.append(uz_field)
    if updated_fields:
        instance.save(update_fields=updated_fields)


def seed_multilingual_content(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    SocialLink = apps.get_model('portfolio', 'SocialLink')
    Skill = apps.get_model('portfolio', 'Skill')
    Service = apps.get_model('portfolio', 'Service')
    Award = apps.get_model('portfolio', 'Award')
    Project = apps.get_model('portfolio', 'Project')
    Testimonial = apps.get_model('portfolio', 'Testimonial')
    BlogPost = apps.get_model('portfolio', 'BlogPost')

    for settings in SiteSettings.objects.all():
        copy_translation_fields(
            settings,
            (
                'site_name',
                'brand_name',
                'meta_description',
                'hero_pre_title',
                'hero_highlight_name',
                'hero_name_suffix',
                'hero_role',
                'about_title',
                'about_description',
                'office_address',
                'call_to_action_text',
                'copyright_text',
            ),
        )
        settings.meta_description_ru = 'Bootstrap шаблон-портфолио, подключенный к Django admin и мультиязычному контенту.'
        settings.meta_description_uz = "Django admin va ko'p tilli kontentga ulangan Bootstrap portfolio shabloni."
        settings.hero_pre_title_ru = 'Я'
        settings.hero_pre_title_uz = 'Men'
        settings.hero_role_ru = 'Фриланс UI/UX дизайнер'
        settings.hero_role_uz = 'Frilans UI/UX dizayner'
        settings.about_title_ru = 'Я создаю продукты, а не просто искусство'
        settings.about_title_uz = "Men shunchaki san'at emas, mahsulot yarataman"
        settings.about_description_ru = (
            'Этот шаблон портфолио подключен к Django admin. '
            'Теперь вы можете редактировать главный экран, услуги, навыки, проекты, отзывы и блог на трех языках.'
        )
        settings.about_description_uz = (
            "Bu portfolio shabloni Django admin bilan ulandi. "
            "Endi bosh sahifa, xizmatlar, ko'nikmalar, loyihalar, fikrlar va blogni uch tilda boshqarishingiz mumkin."
        )
        settings.office_address_ru = 'ул. North 25, Ташкент'
        settings.office_address_uz = "Toshkent, North ko'chasi 25"
        settings.call_to_action_text_ru = 'Давайте поговорим'
        settings.call_to_action_text_uz = 'Keling, gaplashamiz'
        settings.copyright_text_ru = '2026 Follio. Все права защищены.'
        settings.copyright_text_uz = '2026 Follio. Barcha huquqlar himoyalangan.'
        settings.save()

    social_map = {
        'Dribbble': ('Дрибббл', 'Dribbble'),
        'LinkedIn': ('Линкедин', 'LinkedIn'),
        'Instagram': ('Инстаграм', 'Instagram'),
        'Twitter': ('Твиттер', 'Twitter'),
        'Behance': ('Биханс', 'Behance'),
    }
    for social in SocialLink.objects.all():
        copy_translation_fields(social, ('name',))
        if social.name in social_map:
            social.name_ru, social.name_uz = social_map[social.name]
            social.save(update_fields=['name_ru', 'name_uz'])

    skill_map = {
        'Communication Skills': ('Навыки коммуникации', "Muloqot ko'nikmalari"),
        'Project Management': ('Управление проектами', 'Loyiha boshqaruvi'),
        'Problem Solving': ('Решение проблем', 'Muammo yechish'),
        'Analytical Thinking': ('Аналитическое мышление', 'Analitik fikrlash'),
        'Organization': ('Организованность', "Tashkiliy ko'nikma"),
        'Creativity': ('Креативность', 'Ijodkorlik'),
    }
    for skill in Skill.objects.all():
        copy_translation_fields(skill, ('name',))
        if skill.name in skill_map:
            skill.name_ru, skill.name_uz = skill_map[skill.name]
            skill.save(update_fields=['name_ru', 'name_uz'])

    service_map = {
        'Product Design': (
            'Продуктовый дизайн',
            'Mahsulot dizayni',
            'Стратегия продукта, вайрфреймы и продуманные интерфейсные системы.',
            "Mahsulot strategiyasi, wireframe'lar va puxta interfeys tizimlari.",
        ),
        'Web Design': (
            'Веб-дизайн',
            'Veb dizayn',
            'Адаптивный веб-дизайн, где бренд, удобство и производительность работают вместе.',
            "Brend, qulaylik va tezlikni birlashtirgan moslashuvchan veb dizayn.",
        ),
        'Visual Design': (
            'Визуальный дизайн',
            'Vizual dizayn',
            'Сильное визуальное направление для кампаний, лендингов и портфолио.',
            "Kampaniyalar, landing sahifalar va portfolio uchun kuchli vizual yo'nalish.",
        ),
        'Business Strategy': (
            'Бизнес-стратегия',
            'Biznes strategiya',
            'Креативный консалтинг, связывающий потребности клиента с измеримым результатом.',
            "Mijoz ehtiyojlarini o'lchanadigan natija bilan bog'laydigan kreativ konsalting.",
        ),
    }
    for service in Service.objects.all():
        copy_translation_fields(service, ('title', 'description'))
        if service.title in service_map:
            title_ru, title_uz, description_ru, description_uz = service_map[service.title]
            service.title_ru = title_ru
            service.title_uz = title_uz
            service.description_ru = description_ru
            service.description_uz = description_uz
            service.save(update_fields=['title_ru', 'title_uz', 'description_ru', 'description_uz'])

    award_map = {
        'Award One': ('Награда один', '1-mukofot'),
        'Award Two': ('Награда два', '2-mukofot'),
        'Award Three': ('Награда три', '3-mukofot'),
        'Award Four': ('Награда четыре', '4-mukofot'),
    }
    for award in Award.objects.all():
        copy_translation_fields(award, ('title',))
        if award.title in award_map:
            award.title_ru, award.title_uz = award_map[award.title]
            award.save(update_fields=['title_ru', 'title_uz'])

    project_map = {
        'minimalism': {
            'title_ru': 'Минимализм',
            'title_uz': 'Minimalizm',
            'category_ru': 'Иллюстрация . Арт-дирекшн',
            'category_uz': 'Illustratsiya . Art-direkshn',
            'short_description_ru': 'Чистый проект айдентики с уверенной редакционной подачей.',
            'short_description_uz': "Kuchli editorial uslubdagi toza identika loyihasi.",
            'description_ru': 'Minimalism - это проект брендинга и презентации, построенный на ясности, воздухе и уверенной типографике.',
            'description_uz': "Minimalism - bu aniqlik, bo'sh joy va kuchli tipografiyaga qurilgan branding va taqdimot loyihasi.",
            'client_name_ru': 'North Studio',
            'client_name_uz': 'North Studio',
        },
        '3d-project': {
            'title_ru': '3D проект',
            'title_uz': '3D loyiha',
            'category_ru': 'Иллюстрация . Арт-дирекшн',
            'category_uz': 'Illustratsiya . Art-direkshn',
            'short_description_ru': 'Концептуальный визуальный проект с объемной подачей.',
            'short_description_uz': "Konseptual va chuqur vizual taqdimotga ega loyiha.",
            'description_ru': 'Проект сочетает визуальный сторителлинг, 3D-мокапы и подготовленные под анимацию макеты.',
            'description_uz': "Loyiha vizual storytelling, 3D mockup va animatsiyaga mos maketlarni birlashtiradi.",
            'client_name_ru': 'Vertex Labs',
            'client_name_uz': 'Vertex Labs',
        },
        'abstract-art': {
            'title_ru': 'Абстрактное искусство',
            'title_uz': "Abstrakt san'at",
            'category_ru': 'Иллюстрация . Арт-дирекшн',
            'category_uz': 'Illustratsiya . Art-direkshn',
            'short_description_ru': 'Фактурная кампания на стыке современного искусства и digital.',
            'short_description_uz': "Zamonaviy san'at va digital ruhidagi teksturali kampaniya.",
            'description_ru': 'Abstract Art превращает галерейную идею в яркий продуктовый маркетинговый опыт.',
            'description_uz': "Abstract Art galereya g'oyasini yorqin marketing tajribasiga aylantiradi.",
            'client_name_ru': 'Muse Creative',
            'client_name_uz': 'Muse Creative',
        },
        'modern-bg': {
            'title_ru': 'Современный фон',
            'title_uz': 'Zamonaviy fon',
            'category_ru': 'Иллюстрация . Арт-дирекшн',
            'category_uz': 'Illustratsiya . Art-direkshn',
            'short_description_ru': 'Визуальная система с атмосферными фонами и сильными акцентами.',
            'short_description_uz': "Atmosferali fon va kuchli bloklarga ega vizual tizim.",
            'description_ru': 'Modern BG строится на контрасте, модульном контенте и премиальном визуальном тоне.',
            'description_uz': "Modern BG kontrast, modul kontent va premium vizual kayfiyatga qurilgan.",
            'client_name_ru': 'Frame Works',
            'client_name_uz': 'Frame Works',
        },
    }
    for project in Project.objects.all():
        copy_translation_fields(project, ('title', 'category', 'short_description', 'description', 'client_name'))
        translated_values = project_map.get(project.slug)
        if translated_values:
            for field_name, field_value in translated_values.items():
                setattr(project, field_name, field_value)
            project.save(update_fields=list(translated_values.keys()))

    testimonial_map = {
        'John Harry': {
            'role_ru': 'CEO Moderntern',
            'role_uz': 'Moderntern bosh direktori',
            'quote_ru': 'Удобная админка и аккуратная структура превратили шаблон в полноценный продуктовый сайт.',
            'quote_uz': "Qulay admin va toza struktura shablonni to'liq mahsulot saytiga aylantirdi.",
        },
        'Amelia Stone': {
            'role_ru': 'Основатель Studio North',
            'role_uz': 'Studio North asoschisi',
            'quote_ru': 'Быстрая реализация, продуманная структура и фронтенд, который сохранил характер исходного дизайна.',
            'quote_uz': "Tez yakun, puxta struktura va original dizayn ruhini saqlagan frontend.",
        },
        'Daniel Cruz': {
            'role_ru': 'Product Lead в Vertex Labs',
            'role_uz': 'Vertex Labs product lead',
            'quote_ru': 'Возможность редактировать главную страницу и карточки проектов через админку сильно упростила работу.',
            'quote_uz': "Bosh sahifa va loyiha kartalarini admin orqali tahrirlash ishni ancha yengillashtirdi.",
        },
    }
    for testimonial in Testimonial.objects.all():
        copy_translation_fields(testimonial, ('name', 'role', 'quote'))
        translated_values = testimonial_map.get(testimonial.name)
        if translated_values:
            for field_name, field_value in translated_values.items():
                setattr(testimonial, field_name, field_value)
            testimonial.save(update_fields=list(translated_values.keys()))

    blog_map = {
        'helpful-tips-for-becoming-a-successful-designer': {
            'title_ru': 'Полезные советы для успешного дизайнера',
            'title_uz': "Muvaffaqiyatli dizayner bo'lish uchun foydali maslahatlar",
            'author_name_ru': 'Админ',
            'author_name_uz': 'Admin',
            'summary_ru': 'Практические привычки, которые помогают дизайнеру держать качество и темп.',
            'summary_uz': "Dizaynerga sifat va sur'atni ushlab turishga yordam beradigan amaliy odatlar.",
            'content_ru': (
                'Сильный дизайн рождается из повторения, критики и любопытства.\n\n'
                'Стройте системы, а не одиночные экраны. Держите файлы в порядке. Умейте объяснять, почему решение помогает пользователю.\n\n'
                'Настоящий рост начинается там, где вкус превращается в процесс.'
            ),
            'content_uz': (
                "Kuchli dizayn takrorlash, tahlil va qiziqishdan tug'iladi.\n\n"
                "Alohida ekran emas, tizim yarating. Fayllarni tartibli saqlang. Qaror nima uchun foydalanuvchiga foyda berishini tushuntira oling.\n\n"
                "Haqiqiy o'sish did jarayonga aylanganda boshlanadi."
            ),
        },
        'why-structured-admin-content-saves-time-later': {
            'title_ru': 'Почему структурированный контент в админке экономит время',
            'title_uz': 'Strukturali admin kontent keyin nima uchun vaqt tejaydi',
            'author_name_ru': 'Админ',
            'author_name_uz': 'Admin',
            'summary_ru': 'Когда текст шаблона хранится в моделях, обновления становятся быстрее и безопаснее.',
            'summary_uz': "Shablon matnlari modellarda saqlansa, yangilash tezroq va xavfsizroq bo'ladi.",
            'content_ru': (
                'Статичный шаблон хорош для старта, но управляемый из админки контент делает проект живым.\n\n'
                'Когда проекты, услуги и отзывы лежат в базе данных, команда обновляет сайт намного быстрее.'
            ),
            'content_uz': (
                "Statik shablon boshlash uchun qulay, lekin admin orqali boshqariladigan kontent loyihani yashovchan qiladi.\n\n"
                "Loyihalar, xizmatlar va fikrlar bazada bo'lsa, jamoa saytni ancha tez yangilaydi."
            ),
        },
        'from-bootstrap-template-to-django-website': {
            'title_ru': 'От Bootstrap шаблона к Django-сайту',
            'title_uz': 'Bootstrap shablondan Django saytigacha',
            'author_name_ru': 'Админ',
            'author_name_uz': 'Admin',
            'summary_ru': 'Коротко о том, что меняется, когда статическая тема становится рабочим веб-приложением.',
            'summary_uz': "Statik tema ishlaydigan veb ilovaga aylanganda nimalar o'zgarishi haqida qisqacha.",
            'content_ru': (
                'Главное изменение не визуальное, а структурное.\n\n'
                'Views, URLs, templates, models и admin превращают дизайн-ассет в инструмент, с которым команда может работать долго.'
            ),
            'content_uz': (
                "Asosiy o'zgarish vizual emas, strukturaviydir.\n\n"
                "View, URL, template, model va admin dizayn assetini jamoa uzoq muddat boshqara oladigan vositaga aylantiradi."
            ),
        },
    }
    for post in BlogPost.objects.all():
        copy_translation_fields(post, ('title', 'author_name', 'summary', 'content'))
        translated_values = blog_map.get(post.slug)
        if translated_values:
            for field_name, field_value in translated_values.items():
                setattr(post, field_name, field_value)
            post.save(update_fields=list(translated_values.keys()))


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_award_title_ru_award_title_uz_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_multilingual_content, migrations.RunPython.noop),
    ]
