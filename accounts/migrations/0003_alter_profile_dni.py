# Generated by Django 4.2.6 on 2023-10-19 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_profile_avatar_profile_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dni',
            field=models.IntegerField(default=222222, unique=True),
            preserve_default=False,
        ),
    ]
