from django.urls import path
from . import views
from .views import UsernameValidationView, EmailValidationView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/', views.user_settings, name='settings'),
    # path('reset-password/', views.request_reset_password, name='reset-password'),
]

