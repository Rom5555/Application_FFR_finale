from .stock import Stock
from admin_liste.business.entities.modele_liste import ModeleListe
from admin_liste.business.entities.liste_utilisateur import Liste_utilisateur

class Produit:

    def __init__(self):

        self.id = 1
        self.nom = ""
        self.stock = Stock()
        self.quantite_en_stock = 0
        self.modele_liste = ModeleListe()
        self.liste_utilisateur = Liste_utilisateur()
        self.quantite_depart = 0
        self.quantite_retour = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self,value):
        self._nom = value

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self,value):
        self._stock = value

    @property
    def quantite_en_stock(self):
        return self._quantite_en_stock

    @quantite_en_stock.setter
    def quantite_en_stock(self, value):
        self._quantite_en_stock = value

    @property
    def quantite_depart(self):
        return self._quantite_depart

    @quantite_depart.setter
    def quantite_depart(self, value):
        self._quantite_depart = value

    @property
    def quantite_retour(self):
        return self._quantite_retour

    @quantite_retour.setter
    def quantite_retour(self, value):
        self._quantite_retour = value

    @property
    def modele_liste(self):
        return self._modele_liste

    @modele_liste.setter
    def modele_liste(self, value):
        self._modele_liste = value

    @property
    def liste_utilisateur(self):
        return self._liste_utilisateur

    @liste_utilisateur.setter
    def liste_utilisateur(self, value):
        self._liste_utilisateur = value