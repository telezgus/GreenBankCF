# Generated by Django 4.2.6 on 2023-10-19 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_alter_card_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]