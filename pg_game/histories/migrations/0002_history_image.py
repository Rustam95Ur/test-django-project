# Generated by Django 3.1.1 on 2020-12-11 06:40

from django.db import migrations, models
import histories.models


class Migration(migrations.Migration):

    dependencies = [
        ('histories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='image',
            field=models.ImageField(default='img/default_logo.png', null=True, upload_to=histories.models.agent_directory_path, verbose_name='Фото агента'),
        ),
    ]
