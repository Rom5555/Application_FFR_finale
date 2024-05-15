from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'admin_liste'

urlpatterns = [

    path('depart/', views.depart, name='depart'),
    path('remplir_liste_depart/<int:id_liste_depart>/<int:id_produit>/', views.remplir_liste_depart, name='remplir_liste_depart'),
    path('create_liste_utilisateur/<int:id_liste_depart>/', views.create_liste_utilisateur, name='create_liste_utilisateur'),
    path('depart_retour/', views.depart_retour, name='depart_retour'),
    path('retour/', views.retour, name='retour'),
    path('verifier_liste_retour/<int:id_liste_utilisateur>/<int:id_produit>/', views.verifier_liste_retour, name='verifier_liste_retour'),
    path('valider_liste_retour/<int:id_liste_utilisateur>/', views.valider_liste_retour, name='valider_liste_retour'),
    path('liste_utilisateur_creee/', views.liste_utilisateur_creee, name='liste_utilisateur_creee'),
    path('mise_a_jour_stock/', views.mise_a_jour_stock, name='mise_a_jour_stock'),
    path('recherche_archive/', views.recherche_archive, name='recherche_archive'),
    path('display_archive/', views.display_archive, name='display_archive'),
]


