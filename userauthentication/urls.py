from django.urls import path
from . import views
# from .views import UsernameValidationView, EmailValidationView, PasswordValidationView, CustomPasswordChangeView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-password/', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-password'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account-settings/', views.CustomPasswordChangeView.as_view(), name='account-settings'),

    path('reset-password-link/', views.RequestResetPasswordLink.as_view(), name='reset-password-link'),
    # path('set-new-password/', CompletePasswordChange.as_view(), name='set-new-password'),
]

