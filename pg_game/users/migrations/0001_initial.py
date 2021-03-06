# Generated by Django 3.1 on 2020-08-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorAuthList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата попытка')),
                ('login', models.CharField(max_length=50, verbose_name='Логи')),
                ('ip', models.CharField(max_length=50, verbose_name='IP адрес')),
                ('text', models.CharField(max_length=100, verbose_name='Текст ошибки')),
            ],
            options={
                'db_table': 'auth_error_list',
            },
        ),
    ]
