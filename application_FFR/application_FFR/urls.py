"""
URL configuration for application_FFR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView


admin.site.site_header = 'Gestion des comptes'
admin.site.site_title = 'Gestion des comptes'
admin.site.index_title = ''


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(),name='login'),
    path('logistique_service_medical/', include('logistique_service_medical.urls')),
]

