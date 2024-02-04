from django.urls import path
from . import views
# from .views import UsernameValidationView, EmailValidationView, PasswordValidationView, CustomPasswordChangeView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-password/', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-password'),
    path('validate-current-password/', csrf_exempt(views.CurrentPasswordValidationView.as_view()),
         name='validate-current-password'),
    path('set-new-password/', csrf_exempt(views.SetNewPasswordValidationView.as_view()), name='set-new-password'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('account-settings/', views.CustomPasswordChangeView.as_view(), name='account-settings'),

    path('forgot-reset-password/', views.ForgotRequestResetPassword.as_view(),
         name='forgot-reset-password'),
    # path('set-new-password/', CompletePasswordChange.as_view(), name='set-new-password'),
]

