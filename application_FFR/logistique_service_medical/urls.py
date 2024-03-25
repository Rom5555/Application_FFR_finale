from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'logistique_service_medical'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('user_list/', views.user_list, name='user_list'),
    path('add_user/', views.AddUserView.as_view(), name='add_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('consommables/', views.stock_consommables, name='stock_consommables'),
    path('select_stock/', views.select_stock, name='select_stock'),
    path('display_produits/', views.display_produits, name='display_produits'),
    path('produit_list/', views.produit_list, name='produit_list'),
    path('add_produit/', views.add_produit, name='add_produit'),
    path('delete_produit/', views.delete_produit, name='delete_produit'),  # Nouvelle vue pour supprimer un produit
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),  # Utilisation de votre vue d'inscription personnalisée
    path('favoris/', views.favoris, name='favoris'),
    path('update_quantity/<int:id_produit>/', views.update_quantity, name='update_quantity'),
    path('liste_depart/', views.liste_depart, name='liste_depart'),
    path('logistique_service_medical/remplir_liste_depart/<int:id_liste_depart>/<int:id_produit>/', views.remplir_liste_depart, name='remplir_liste_depart'),
]


