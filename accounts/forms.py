from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserCreationFormWithProfile(UserCreationForm):
    dni = forms.CharField(label='DNI', max_length=50, help_text='', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password1 = None
    password2 = None
    username = forms.CharField(label='Username', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus':'autofocus'}))
    first_name = forms.CharField(label='First Name', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_dni(self):
        data = self.cleaned_data['dni']
        if Profile.objects.filter(dni=data).exists():
            raise forms.ValidationError("A user with that DNI already exists")
        return data
        
    
    class Meta:
        model = User
        fields = ['username', 'dni' , 'first_name', 'last_name']
        
    
        
