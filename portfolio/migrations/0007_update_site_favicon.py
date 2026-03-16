from django.db import migrations, models


NEW_FAVICON_PATH = 'assets/images/site-favicon.png'
LEGACY_FAVICON_PATHS = {
    '',
    'assets/images/favicon.png',
}


def update_site_favicon_path(apps, schema_editor):
    SiteSettings = apps.get_model('portfolio', 'SiteSettings')
    for site_settings in SiteSettings.objects.all():
        if site_settings.favicon_image in LEGACY_FAVICON_PATHS:
            site_settings.favicon_image = NEW_FAVICON_PATH
            site_settings.save(update_fields=['favicon_image'])


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0006_award_image_path_file_blogpost_image_path_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='favicon_image',
            field=models.CharField(default=NEW_FAVICON_PATH, max_length=255),
        ),
        migrations.RunPython(update_site_favicon_path, migrations.RunPython.noop),
    ]
