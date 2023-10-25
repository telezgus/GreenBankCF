from django import forms
from django.core.validators import RegexValidator
from .models import Card
from django.core.validators import MinValueValidator, MaxValueValidator


class TransactionForm(forms.Form): 
    alias = forms.CharField(max_length=100)
    amount = forms.IntegerField()
    pin = forms.CharField(
            max_length=4,  # Define la longitud máxima como 4 caracteres
            validators=[
                RegexValidator(
                    regex=r'^\d{4}$',  # Expresión regular que coincide con 4 dígitos
                    message="El campo debe contener exactamente 4 dígitos.",
                ),
            ]
        )
        


class NewCardForm(forms.Form):
    dni = forms.IntegerField(label='DNI', validators=[MinValueValidator(1000000, message= "DNI too short"), MaxValueValidator(99999999,message= "DNI not valid")])



class DeleteCardForm(forms.Form):
    card_number = forms.IntegerField(validators=[MinValueValidator(1000000000000000, message= "Card number must have 16 digits"), MaxValueValidator(9999999999999999,message= "Card number must have 16 digits")])
    dni = forms.IntegerField(label="DNI", validators=[MinValueValidator(1000000, message= "DNI too short"), MaxValueValidator(99999999,message= "DNI not valid")])


class ChangeAlias(forms.Form):
    alias = forms.CharField(max_length=100)