from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'admin_compte'

urlpatterns = [

    path('user_list/', views.user_list, name='user_list'),
    path('add_user/', views.AddUserView.as_view(), name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('register/', views.RegisterView.as_view(), name='register'),  # Utilisation de votre vue d'inscription personnalisée

]


