from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'registration'

urlpatterns = [

    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),  # Utilisation de votre vue d'inscription personnalisée
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


