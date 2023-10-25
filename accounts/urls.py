from django.contrib import admin
from django.urls import path

from .views import login_view ,profile, logout_view, signup_view, inactivity_logout

urlpatterns = [
    path('profile', profile, name='profile'),
    path('', login_view , name = 'login'),
    path('logout', logout_view , name = 'logout'),
    path('signup', signup_view , name = 'signup'),
    path('inactivity_logout', inactivity_logout , name = 'inactivity_logout')
    
]
