# Generated by Django 3.1.3 on 2020-11-26 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201126_1514'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievements',
            name='header',
        ),
        migrations.AddField(
            model_name='achievements',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievements',
            name='label',
            field=models.TextField(default='', unique=True),
            preserve_default=False,
        ),
    ]