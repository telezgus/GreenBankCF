# Generated by Django 4.2.6 on 2023-10-14 19:02

import cards.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='alias',
            field=models.CharField(default=cards.models.random_alias, max_length=100),
        ),
    ]
