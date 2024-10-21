from django.urls import path
from . import views

app_name = 'admin_liste'

urlpatterns = [
    path('recherche_modele_liste/', views.recherche_modele_liste, name='recherche_modele_liste'),
    path('create_modele_liste/', views.create_modele_liste, name='create_modele_liste'),
    path('remplir_modele_liste/<int:id_modele_liste>/<int:id_produit>/', views.remplir_modele_liste, name='remplir_modele_liste'),
    path('depart/', views.depart, name='depart'),
    path('remplir_liste_utilisateur/<int:id_liste_utilisateur>/<int:id_produit>/', views.remplir_liste_utilisateur, name='remplir_liste_utilisateur'),
    path('create_liste_utilisateur/<int:id_liste_utilisateur>/', views.create_liste_utilisateur, name='create_liste_utilisateur'),
    path('depart_retour/', views.depart_retour, name='depart_retour'),
    path('retour/', views.retour, name='retour'),
    path('verifier_liste_retour/<int:id_liste_utilisateur>/<int:id_produit>/', views.verifier_liste_retour, name='verifier_liste_retour'),
    path('valider_liste_retour/<int:id_liste_utilisateur>/', views.valider_liste_retour, name='valider_liste_retour'),
    path('liste_utilisateur_creee/', views.liste_utilisateur_creee, name='liste_utilisateur_creee'),
    path('mise_a_jour_stock/', views.mise_a_jour_stock, name='mise_a_jour_stock'),
    path('recherche_archive/', views.recherche_archive, name='recherche_archive'),
    path('display_archive/', views.display_archive, name='display_archive'),
]


