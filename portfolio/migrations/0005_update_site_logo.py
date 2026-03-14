from django.db import migrations, models


NEW_LOGO_PATH = 'assets/images/site-logo.png'
LEGACY_LOGO_PATHS = {
    '',
    'assets/images/logo.png',
    'assets/images/logo2.png',
    'assets/images/logo3.png',
}


def update_site_logo_paths(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    for site_settings in SiteSettings.objects.all():
        if site_settings.logo_image in LEGACY_LOGO_PATHS:
            site_settings.logo_image = NEW_LOGO_PATH
        if site_settings.footer_logo_image in LEGACY_LOGO_PATHS:
            site_settings.footer_logo_image = NEW_LOGO_PATH
        site_settings.save(update_fields=['logo_image', 'footer_logo_image'])


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_seed_multilingual_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='footer_logo_image',
            field=models.CharField(default=NEW_LOGO_PATH, max_length=255),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='logo_image',
            field=models.CharField(default=NEW_LOGO_PATH, max_length=255),
        ),
        migrations.RunPython(update_site_logo_paths, migrations.RunPython.noop),
    ]
