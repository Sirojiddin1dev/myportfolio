from django.utils import translation


LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('ru', 'Русский'),
    ('uz', "O'zbek"),
)

DEFAULT_LANGUAGE = 'en'
SUPPORTED_LANGUAGE_CODES = {code for code, _label in LANGUAGE_CHOICES}

UI_TEXTS = {
    'home': {'en': 'Home', 'ru': 'Главная', 'uz': 'Bosh sahifa'},
    'about': {'en': 'About', 'ru': 'О нас', 'uz': 'Men haqimda'},
    'portfolio': {'en': 'Portfolio', 'ru': 'Портфолио', 'uz': 'Portfolio'},
    'blog': {'en': 'Blog', 'ru': 'Блог', 'uz': 'Blog'},
    'contact': {'en': 'Contact', 'ru': 'Контакты', 'uz': 'Aloqa'},
    'admin': {'en': 'Admin', 'ru': 'Админ', 'uz': 'Admin'},
    'years': {'en': 'Years', 'ru': 'Лет', 'uz': 'Yil'},
    'experience': {'en': 'Experience', 'ru': 'Опыта', 'uz': 'Tajriba'},
    'about_me': {'en': 'About Me', 'ru': 'Обо мне', 'uz': 'Men haqimda'},
    'about_tab': {'en': 'About', 'ru': 'О нас', 'uz': 'Haqida'},
    'skill': {'en': 'Skill', 'ru': 'Навык', 'uz': "Ko'nikma"},
    'skills': {'en': 'Skills', 'ru': 'Навыки', 'uz': "Ko'nikmalar"},
    'services': {'en': 'Services', 'ru': 'Услуги', 'uz': 'Xizmatlar'},
    'social_media': {'en': 'Social Media', 'ru': 'Соцсети', 'uz': 'Ijtimoiy tarmoqlar'},
    'award': {'en': 'Award', 'ru': 'Награда', 'uz': 'Mukofot'},
    'awards': {'en': 'Awards', 'ru': 'Награды', 'uz': 'Mukofotlar'},
    'view_work': {'en': 'View Work', 'ru': 'Смотреть работу', 'uz': "Ishni ko'rish"},
    'see_more_work': {'en': 'See More Work...', 'ru': 'Смотреть еще работы...', 'uz': "Yana ishlarni ko'rish..."},
    'testimonial': {'en': 'Testimonial', 'ru': 'Отзывы', 'uz': 'Mijozlar fikri'},
    'latest_news': {'en': 'Latest News', 'ru': 'Последние новости', 'uz': "So'nggi yangiliklar"},
    'by': {'en': 'By', 'ru': 'Автор', 'uz': 'Muallif'},
    'read_more': {'en': 'Read More...', 'ru': 'Читать далее...', 'uz': 'Batafsil...'},
    'creative_profile_and_capabilities': {'en': 'Creative profile and capabilities', 'ru': 'Творческий профиль и возможности', 'uz': 'Ijodiy profil va imkoniyatlar'},
    'experience_label': {'en': 'Experience', 'ru': 'Опыт', 'uz': 'Tajriba'},
    'contact_label': {'en': 'Contact', 'ru': 'Контакт', 'uz': 'Aloqa'},
    'capability': {'en': 'Capability', 'ru': 'Навык', 'uz': 'Daraja'},
    'proficiency': {'en': 'proficiency', 'ru': 'уровень', 'uz': 'daraja'},
    'selected_client_work_and_case_studies': {'en': 'Selected client work and case studies', 'ru': 'Избранные клиентские работы и кейсы', 'uz': 'Tanlangan ishlar va кейсlar'},
    'view_project': {'en': 'View Project', 'ru': 'Смотреть проект', 'uz': "Loyihani ko'rish"},
    'no_projects': {'en': 'No projects yet. Add some from admin.', 'ru': 'Проектов пока нет. Добавьте их через админку.', 'uz': "Hozircha loyiha yo'q. Admin orqali qo'shing."},
    'project_info': {'en': 'Project Info', 'ru': 'Информация о проекте', 'uz': "Loyiha ma'lumoti"},
    'category': {'en': 'Category', 'ru': 'Категория', 'uz': 'Kategoriya'},
    'client': {'en': 'Client', 'ru': 'Клиент', 'uz': 'Mijoz'},
    'summary': {'en': 'Summary', 'ru': 'Кратко', 'uz': 'Qisqacha'},
    'open_project': {'en': 'Open Project', 'ru': 'Открыть проект', 'uz': 'Loyihani ochish'},
    'related_projects': {'en': 'Related Projects', 'ru': 'Похожие проекты', 'uz': "O'xshash loyihalar"},
    'latest_notes_ideas_and_updates': {'en': 'Latest notes, ideas, and updates', 'ru': 'Последние заметки, идеи и обновления', 'uz': "So'nggi yozuvlar, g'oyalar va yangilanishlar"},
    'read_article': {'en': 'Read Article', 'ru': 'Читать статью', 'uz': "Maqolani o'qish"},
    'no_blog_posts': {'en': 'No blog posts yet. Add some from admin.', 'ru': 'Публикаций пока нет. Добавьте их через админку.', 'uz': "Hozircha maqolalar yo'q. Admin orqali qo'shing."},
    'more_articles': {'en': 'More Articles', 'ru': 'Еще статьи', 'uz': "Yana maqolalar"},
    'start_conversation_about_your_next_project': {'en': 'Start a conversation about your next project', 'ru': 'Начните разговор о вашем следующем проекте', 'uz': 'Keyingi loyihangiz haqida suhbatni boshlang'},
    'get_in_touch': {'en': 'Get In Touch', 'ru': 'Связаться', 'uz': "Bog'lanish"},
    'send_message': {'en': 'Send Message', 'ru': 'Отправить сообщение', 'uz': 'Xabar yuborish'},
    'office_address': {'en': 'Office Address', 'ru': 'Адрес офиса', 'uz': 'Ofis manzili'},
    'official_mail': {'en': 'Official Mail', 'ru': 'Официальная почта', 'uz': 'Rasmiy email'},
    'official_phone': {'en': 'Official Phone', 'ru': 'Официальный телефон', 'uz': 'Rasmiy telefon'},
    'contact_success': {'en': 'Your message has been sent successfully.', 'ru': 'Ваше сообщение успешно отправлено.', 'uz': 'Xabaringiz muvaffaqiyatli yuborildi.'},
    'first_name': {'en': 'First Name', 'ru': 'Имя', 'uz': 'Ism'},
    'last_name': {'en': 'Last Name', 'ru': 'Фамилия', 'uz': 'Familiya'},
    'email': {'en': 'Email', 'ru': 'Эл. почта', 'uz': 'Email'},
    'subject': {'en': 'Subject', 'ru': 'Тема', 'uz': 'Mavzu'},
    'message_placeholder': {'en': 'Project description...', 'ru': 'Описание проекта...', 'uz': "Loyiha tavsifi..."},
    'add_social_links': {'en': 'Add social links in admin.', 'ru': 'Добавьте ссылки на соцсети в админке.', 'uz': "Social linklarni admindan qo'shing."},
    'add_skills': {'en': 'Add skills from admin to populate this section.', 'ru': 'Добавьте навыки из админки для этого раздела.', 'uz': "Bu bo'limni to'ldirish uchun admindan ko'nikmalar qo'shing."},
    'add_services': {'en': 'Add services from admin to populate this section.', 'ru': 'Добавьте услуги из админки для этого раздела.', 'uz': "Bu bo'limni to'ldirish uchun admindan xizmatlar qo'shing."},
    'add_awards': {'en': 'Add awards from admin to populate this section.', 'ru': 'Добавьте награды из админки для этого раздела.', 'uz': "Bu bo'limni to'ldirish uchun admindan mukofotlar qo'shing."},
    'add_testimonials': {'en': 'Add testimonials from admin to populate this slider.', 'ru': 'Добавьте отзывы из админки для этого слайдера.', 'uz': "Bu slayder uchun admindan fikrlar qo'shing."},
    'add_blog_posts': {'en': 'Add blog posts from admin to populate this section.', 'ru': 'Добавьте статьи из админки для этого раздела.', 'uz': "Bu bo'limni to'ldirish uchun admindan maqolalar qo'shing."},
}


def normalize_language_code(language_code):
    normalized = (language_code or DEFAULT_LANGUAGE).split('-')[0].lower()
    return normalized if normalized in SUPPORTED_LANGUAGE_CODES else DEFAULT_LANGUAGE


def get_current_language(request=None):
    if request is not None and getattr(request, 'current_language', None):
        return normalize_language_code(request.current_language)
    return normalize_language_code(translation.get_language())


def get_ui_text(key, language_code=None):
    normalized_language = normalize_language_code(language_code)
    key_map = UI_TEXTS.get(key, {})
    return key_map.get(normalized_language) or key_map.get(DEFAULT_LANGUAGE) or key


def get_ui_bundle(language_code=None):
    normalized_language = normalize_language_code(language_code)
    return {key: get_ui_text(key, normalized_language) for key in UI_TEXTS}


def translate_model_field(instance, field_name, language_code=None):
    normalized_language = normalize_language_code(language_code or get_current_language())
    if hasattr(instance, 'get_translated'):
        return instance.get_translated(field_name, normalized_language)
    return getattr(instance, field_name, '')
