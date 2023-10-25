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
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
        logout(request)
        return render(request, 'accounts/logout.html')


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
@permission_required('auth.add_user',raise_exception=True)
def signup_view(request):
    if request.method=='POST':
        form = UserCreationFormWithProfile(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='client')
            password = User.objects.make_random_password()
            form.cleaned_data['password1'] = password
            form.cleaned_data['password2'] = password
            new_user=form.save()
            new_user.groups.add(group)
            dni = form.cleaned_data['dni']
            Profile.objects.create(user=new_user, dni=dni)
            new_user.save()
            return render(request, 'accounts/signup_ok.html', {'new_user': new_user,'password':password})             
    else:
        form = UserCreationFormWithProfile()
    return render(request, 'accounts/signup.html', {'form' : form}) 


def inactivity_logout(request):
    return render(request,'accounts/inactivity_logout.html', status=403)