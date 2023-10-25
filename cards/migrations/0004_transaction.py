# Generated by Django 4.2.6 on 2023-10-13 23:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_card_card_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('receiver_card', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='reciver', to='cards.card')),
                ('sender_card', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sender', to='cards.card')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
    ]