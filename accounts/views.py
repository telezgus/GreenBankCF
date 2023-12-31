from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.models import User
from .forms import UserCreationFormWithProfile



def login_view(request):
    """Login logic for users using AuthenticationForm.
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request , user)
            if user.groups.filter(name='client'):
                return redirect('cards')
            else:
                return redirect('new_card')
    else:
        if request.user.is_authenticated:
            return redirect('cards')
        else:
            form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Logout users logic.
    """
    logout(request)
    return render(request, 'accounts/logout.html')


@login_required
def profile(request):
    """Renders users to profile page.
    """
    return render(request, 'accounts/profile.html')

@login_required
@permission_required('auth.add_user',raise_exception=True)
def signup_view(request):
    """Validates and creates a new user using UserCreationFormWithProfile.
    """
    if request.method=='POST':
        form = UserCreationFormWithProfile(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='client')
            password = User.objects.make_random_password() # Generates new random password
            form.cleaned_data['password1'] = password
            form.cleaned_data['password2'] = password
            new_user=form.save()
            new_user.groups.add(group)
            dni = form.cleaned_data['dni']
            Profile.objects.create(user=new_user, dni=dni) # Creates profile for user
            new_user.save()
            return render(request, 'accounts/signup_ok.html', {'new_user': new_user,'password':password})             
    else:
        form = UserCreationFormWithProfile()
    return render(request, 'accounts/signup.html', {'form' : form}) 


def inactivity_logout(request):
    """Redirects user to logged out due to incactivity page.
    """
    return render(request,'accounts/inactivity_logout.html', status=403)