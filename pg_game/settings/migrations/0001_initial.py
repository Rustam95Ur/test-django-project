# Generated by Django 3.1.1 on 2020-12-04 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=225, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус')),
            ],
            options={
                'db_table': 'upload_group_setting',
            },
        ),
        migrations.CreateModel(
            name='UploadSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(verbose_name='Тип настройки')),
                ('title', models.CharField(max_length=100, null=True, verbose_name='Название')),
                ('col_name', models.CharField(max_length=200, unique=True, verbose_name='Название колоны')),
                ('type_val', models.CharField(max_length=100, null=True, verbose_name='Tип ранга')),
                ('value', models.CharField(max_length=200, null=True, verbose_name='Значение')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='settings.groupsetting', verbose_name='Связь с группой')),
            ],
            options={
                'db_table': 'upload_setting',
            },
        ),
    ]
