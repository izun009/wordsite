# Generated by Django 3.2.11 on 2022-02-04 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20220204_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogauthor',
            options={'verbose_name': 'Author', 'verbose_name_plural': 'Authors'},
        ),
    ]