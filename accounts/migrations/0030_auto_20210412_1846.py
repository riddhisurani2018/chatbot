# Generated by Django 3.1.7 on 2021-04-12 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_delete_manual_response_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='text_keyword',
            name='keyword_value',
            field=models.TextField(help_text='Enter keyword here', verbose_name='Keyword'),
        ),
    ]
