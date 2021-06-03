# Generated by Django 3.1.7 on 2021-03-22 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20210313_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='manual_response',
            name='email_id',
            field=models.EmailField(default='Default User', max_length=254, verbose_name='Added By'),
        ),
        migrations.AlterField(
            model_name='link_keyword',
            name='keyword_values',
            field=models.CharField(help_text='Enter keyword here', max_length=100, verbose_name='Keyword'),
        ),
        migrations.AlterField(
            model_name='link_keyword',
            name='links',
            field=models.CharField(help_text='Enter corresponding link here', max_length=1000, verbose_name='Link'),
        ),
        migrations.AlterField(
            model_name='text_keyword',
            name='desc',
            field=models.TextField(help_text='Enter corresponding response here', verbose_name='Intent'),
        ),
        migrations.AlterField(
            model_name='text_keyword',
            name='keyword_value',
            field=models.CharField(help_text='Enter keyword here', max_length=100, verbose_name='Keyword'),
        ),
    ]