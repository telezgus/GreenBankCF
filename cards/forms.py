from django import forms
from django.core.validators import RegexValidator
from .models import Card
from django.core.validators import MinValueValidator, MaxValueValidator


class TransactionForm(forms.Form): 
    """Form to create new transaction
    """
    alias = forms.CharField(label='Alias',
                            max_length=50,
                            help_text='',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.IntegerField(label='Amount',
                                help_text='',
                                min_value=1,
                                error_messages={'min_value': 'Invalid amount'},
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    pin = forms.CharField(
            max_length=4,
            label='PIN',
            widget=forms.NumberInput(attrs={'class': 'form-control'}),
            validators=[
                RegexValidator(
                    regex=r'^\d{4}$',  # Regular explession for 4 digits.
                    message="This field must contain 4 digits.",
                ),
            ]
        )
        


class NewCardForm(forms.Form):
    """Form to create new card. 
    - DNI must be 7 or 8 digits long.
    """
    dni = forms.IntegerField(
                            label='DNI', 
                            validators=[MinValueValidator(1000000, 
                                                          message= "DNI too short"),
                                        MaxValueValidator(99999999,
                                                          message= "DNI not valid")
                                        ]
                            )



class DeleteCardForm(forms.Form):
    """Form to delete a card.
    - Card number must have 16 digits.
    - DNI must be 7 or 8 digits long.
    """
    card_number = forms.IntegerField(label='Card Number',
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                     validators=[MinValueValidator(1000000000000000, message= "Card number must have 16 digits"), MaxValueValidator(9999999999999999,message= "Card number must have 16 digits")])
    dni = forms.IntegerField(label="DNI",
                             widget=forms.NumberInput(attrs={'class': 'form-control'}),
                             validators=[MinValueValidator(1000000, message= "DNI too short"), MaxValueValidator(99999999,message= "DNI not valid")])


class ChangeAlias(forms.Form):
    """Form for alias changing
    """
    alias = forms.CharField(max_length=100)