# Generated by Django 3.1.3 on 2020-11-07 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20201107_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='get_point_multiplier',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='give_point_multiplier',
            field=models.IntegerField(default=1),
        ),
    ]