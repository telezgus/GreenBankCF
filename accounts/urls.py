from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view ,profile, logout_view, signup_view, inactivity_logout

urlpatterns = [
    path('profile', profile, name='profile'),
    path('', login_view , name = 'login'),
    path('logout', logout_view , name = 'logout'),
    path('signup', signup_view , name = 'signup'),
    path('inactivity_logout', inactivity_logout , name = 'inactivity_logout'),
    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name='password_reset'),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), 
        name="password_reset_complete"),
    
]
