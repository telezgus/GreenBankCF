from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
import random
from random_word import RandomWords


def random_alias():
    r = RandomWords()
    a = r.get_random_word() 
    b = r.get_random_word()
    c = r.get_random_word()
    return f'{a}.{b}.{c}'
    
    
def random_pin():
    return str(random.randint(0000, 9999))

def get_expiring_date():
    actual_date = timezone.now()
    expiring_date = actual_date + timedelta(days = 365 * 4)
    return expiring_date
    
# Extending User Model Using a One-To-One Link
class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.BigIntegerField(null=True,unique=True)
    alias = models.CharField(max_length=100, default=random_alias,unique=True)
    pin= models.CharField(
            default= random_pin,
            max_length=4,  # Define la longitud máxima como 4 caracteres
            validators=[
                RegexValidator(
                    regex=r'^\d{4}$',  # Expresión regular que coincide con 4 dígitos
                    message="El campo debe contener exactamente 4 dígitos.",
                ),
            ]
        )
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    expiring_date = models.DateTimeField(default=get_expiring_date)
    
    @property
    def format_expiring_date(self):
        return self.expiring_date.strftime('%m/%y')

    def __str__(self):
        return str(self.card_number)
    
    
    
class Transaction(models.Model):
    sender_card = models.ForeignKey(Card,
                                    on_delete=models.SET_DEFAULT,
                                    default=None,
                                    related_name='sender'
                                    )
    receiver_card = models.ForeignKey(Card,
                                      on_delete=models.SET_DEFAULT,
                                      default=None,
                                      related_name='reciver'
                                      )
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateTimeField(default=timezone.now)
    

    class Meta:
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")

    
        