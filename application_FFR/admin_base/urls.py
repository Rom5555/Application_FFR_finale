from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'admin_base'

urlpatterns = [

    path('index/', views.index, name='index'),

]


