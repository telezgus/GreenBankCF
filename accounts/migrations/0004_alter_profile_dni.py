# Generated by Django 4.2.6 on 2023-10-19 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_dni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dni',
            field=models.IntegerField(error_messages={'unique': 'DNI already exists'}, unique=True),
        ),
    ]
