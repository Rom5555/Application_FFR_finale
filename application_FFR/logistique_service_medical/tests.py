from django.test import TestCase
from django.db.utils import IntegrityError
from .models import CategorieProduit, Produit, User, Deplacement, Stock, ListeDepart

class ModelTests(TestCase):
    def setUp(self):
        self.categorie = CategorieProduit.objects.create(nom_categorie_produit="Nourriture")

    def test_create_produit(self):
        produit = Produit.objects.create(nom_produit="Pain", id_categorie_produit=self.categorie)
        self.assertIsNotNone(produit.id_produit)

    def test_retrieve_user(self):
        utilisateur = User.objects.create(nom="Nom_utilisateur", prenom="Prenom_utilisateur", mail="utilisateur@example.com", mot_de_passe="password")
        retrieved_user = User.objects.get(id_utilisateur=utilisateur.id_utilisateur)
        self.assertEqual(retrieved_user.mail, "utilisateur@example.com")

    def test_update_stock(self):
        stock = Stock.objects.create(nom_stock="Ancien_nom_stock")
        stock.nom_stock = "Nouveau_nom_stock"
        stock.save()
        updated_stock = Stock.objects.get(id_stock=stock.id_stock)
        self.assertEqual(updated_stock.nom_stock, "Nouveau_nom_stock")

    def test_delete_deplacement(self):
        deplacement = Deplacement.objects.create(nombre_joueurs=15, duree_deplacement=5, nombre_match=2)
        deplacement.delete()
        with self.assertRaises(Deplacement.DoesNotExist):
            Deplacement.objects.get(id_deplacement=deplacement.id_deplacement)

    def test_unique_categorie_produit(self):
        with self.assertRaises(IntegrityError):
            CategorieProduit.objects.create(nom_categorie_produit="Nourriture")
            CategorieProduit.objects.create(nom_categorie_produit="Nourriture")

