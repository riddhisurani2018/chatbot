# Generated by Django 3.1.7 on 2021-03-11 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210311_0521'),
    ]

    operations = [
        migrations.CreateModel(
            name='manual_response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_keyword', models.CharField(max_length=100, verbose_name='Non-Database Keywords')),
                ('admin_data', models.TextField(verbose_name='Admin Response')),
            ],
            options={
                'verbose_name': 'manual response',
                'verbose_name_plural': 'Manual Responses',
            },
        ),
    ]
