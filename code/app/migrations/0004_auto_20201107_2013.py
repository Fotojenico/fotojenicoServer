# Generated by Django 3.1.3 on 2020-11-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_profile_point_multiplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='point_multiplier',
            field=models.IntegerField(default=1),
        ),
    ]