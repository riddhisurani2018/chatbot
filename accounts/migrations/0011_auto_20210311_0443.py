# Generated by Django 3.1.7 on 2021-03-11 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20210311_0439'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='text_keyword',
            new_name='link_keyword',
        ),
    ]
