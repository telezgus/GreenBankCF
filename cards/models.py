from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator, MinValueValidator
import random
from random_word import RandomWords


def random_alias():
    """Generates randon alias (3 random words, dot separated)
    """
    r = RandomWords()
    a = r.get_random_word() 
    b = r.get_random_word()
    c = r.get_random_word()
    alias = f'{a}.{b}.{c}'
    return check_alias_uniqueness(alias)

def check_alias_uniqueness(alias):
    """Checks alias uniqueness (if not unique, generates a new one and checks again)
    """
    if Card.objects.filter(alias=alias).exists():
        return random_alias()
    else:
        return alias

    
def random_pin():
    """Generates randon pin (4 digits integer)
    """
    return str(random.randint(0000, 9999))

def get_expiring_date():
    """Calculates expiration card date (4 years since card creation date)
    """
    actual_date = timezone.now()
    expiring_date = actual_date + timedelta(days = 365 * 4)
    return expiring_date


    
# Extending User Model Using a One-To-One Link
class Card(models.Model):
    """Card model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.BigIntegerField(null=True,unique=True)
    alias = models.CharField(max_length=100, default=random_alias,unique=True)
    pin= models.CharField(
            default= random_pin,
            max_length=4,  # Max lenght 4 characters
            validators=[
                RegexValidator(
                    regex=r'^\d{4}$',  # Regular explession for 4 digits
                    message="Field must contain exactly 4 digits.",
                ),
            ]
        )
    total_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    expiring_date = models.DateTimeField(default=get_expiring_date)
    
    @property
    def format_expiring_date(self):
        """Adds a property that returns expiring date in m/y format
        """
        return self.expiring_date.strftime('%m/%y')
    
    @property
    def format_card_number(self):
        """Adds a property that returns formated card number
        """
        return ' '.join([str(self.card_number)[i:i+4] for i in range(0, len(str(self.card_number)), 4)])
    

    def __str__(self):
        """Returns card number when __str__ function is called
        """
        return str(self.card_number)
    
    
    
class Transaction(models.Model):
    "Trnsaction model"
    sender_card = models.ForeignKey(Card,
                                    on_delete=models.CASCADE,related_name='sender_card'
                                    )
    receiver_card = models.ForeignKey(Card,
                                      on_delete=models.CASCADE, related_name='receiver_card'
                                      )
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0, message='Invalid amount')])
    date = models.DateTimeField(default=timezone.now)
    confirmed = models.BooleanField(default=False)
    

    class Meta:
        """Metadata defining singular and plural class name
        """
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")

    
        