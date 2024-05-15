from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'admin_stock'

urlpatterns = [

    path('consommables/', views.stock_consommables, name='stock_consommables'),
    path('select_stock/', views.select_stock, name='select_stock'),
    path('display_produits/', views.display_produits, name='display_produits'),
    path('update_quantity/<int:id_produit>/', views.update_quantity, name='update_quantity'),
    path('produit_list/', views.produit_list, name='produit_list'),
    path('add_produit/', views.add_produit, name='add_produit'),
    path('delete_produit/', views.delete_produit, name='delete_produit'),

]