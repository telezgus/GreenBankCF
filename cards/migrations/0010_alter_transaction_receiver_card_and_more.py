# Generated by Django 4.2.6 on 2023-11-08 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0009_alter_transaction_receiver_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='receiver_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_card', to='cards.card'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_card', to='cards.card'),
        ),
    ]
