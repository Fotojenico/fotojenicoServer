# Generated by Django 3.1.4 on 2020-12-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20201202_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievements',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='achievements',
            name='title',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]