# Generated by Django 3.1.7 on 2021-03-09 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210309_1211'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='About_U',
            new_name='About_Us',
        ),
        migrations.AlterModelOptions(
            name='about_us',
            options={'verbose_name': 'About U'},
        ),
        migrations.AlterModelOptions(
            name='text_keyword',
            options={'verbose_name': 'Text Keyword and Intent'},
        ),
    ]
