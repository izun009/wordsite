# Generated by Django 3.2.11 on 2022-02-06 22:11

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220205_2053'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blogpage',
            managers=[
                ('relatetags', django.db.models.manager.Manager()),
            ],
        ),
    ]
