# Generated by Django 4.2.6 on 2023-11-03 19:12

import cards.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_card_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='pin',
            field=models.CharField(default=cards.models.random_pin, max_length=4, validators=[django.core.validators.RegexValidator(message='Field must contain exactly 4 digits.', regex='^\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver_card',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reciver', to='cards.card'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender_card',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sender', to='cards.card'),
        ),
    ]
