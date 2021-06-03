# Generated by Django 2.2.12 on 2021-03-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_text_keyword_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='manual_response_manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='about_us',
            name='about_us_paragraph',
            field=models.TextField(help_text='Enter about us here', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='text_keyword',
            name='tag',
            field=models.CharField(choices=[('consult', 'Consult'), ('knowledge', 'Knowledge'), ('contact', 'Contact'), ('noanswer', 'No Answer'), ('options', 'Options')], default='noanswer', help_text='Provide relevant tag here', max_length=10),
        ),
    ]
