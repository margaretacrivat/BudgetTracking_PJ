from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-password/', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-password'),

    path('login/', views.user_login, name='login'),
    path('forgot-reset-password/', views.ForgotRequestResetPassword.as_view(),
         name='forgot-reset-password'),
    path('logout/', views.user_logout, name='logout'),
    path('account-settings/', views.set_new_password, name='account-settings'),
    path('delete-account/<int:pk>/', views.DeleteUserAccount.as_view(), name='delete-account'),
]

