from django.urls import path
from . import views

app_name = 'user_liste'

urlpatterns = [

    path('display_ma_liste/', views.display_ma_liste, name='display_ma_liste'),
    path('remplir_liste_retour/<int:id_liste_utilisateur>/<int:id_produit>/', views.remplir_liste_retour, name='remplir_liste_retour'),

]


