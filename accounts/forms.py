from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserCreationFormWithProfile(UserCreationForm):
    """User creation form.
    
        Password is automatically generated and asigned in .views.signup_view method
    """
    dni = forms.CharField(label='DNI', max_length=50, help_text='', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=254, help_text='', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = None    #Removes password from form inputs.
    password2 = None    #Removes password from form inputs.
    username = forms.CharField(label='Username', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus':'autofocus'}))
    first_name = forms.CharField(label='First Name', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', max_length=50, help_text='', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_dni(self):
        """Check if DNI number is already registrated (must be unique).

        Raises:
            forms.ValidationError: Error if DIN already exists).

        Returns:
            data: Validated data.
        """
        data = self.cleaned_data['dni']
        if Profile.objects.filter(dni=data).exists():
            raise forms.ValidationError("A user with that DNI already exists")
        return data
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registrated.")
        return email
        
    
    class Meta:
        """Select fields to be displayed in form inputs.
        """
        model = User
        fields = ['username', 'dni' , 'first_name', 'last_name','email']
        
    
        
