from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'user_liste'

urlpatterns = [

    path('index_utilisateur/', views.index_utilisateur, name='index_utilisateur'),
    path('ma_liste/', views.ma_liste, name='ma_liste'),
    path('remplir_liste_retour/<int:id_liste_utilisateur>/<int:id_produit>/', views.remplir_liste_retour, name='remplir_liste_retour'),

]


