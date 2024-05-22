from .stock import Stock
from admin_liste.business.entities.liste_depart import Liste_depart
from admin_liste.business.entities.liste_utilisateur import Liste_utilisateur

class Produit:

    def __init__(self):

        self.id = 1
        self.nom = ""
        self.stock = Stock()
        self.quantite_en_stock = 0
        self.liste_depart = Liste_depart()
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
    def liste_depart(self):
        return self._liste_depart

    @liste_depart.setter
    def liste_depart(self, value):
        self._liste_depart = value

    @property
    def liste_utilisateur(self):
        return self._liste_utilisateur

    @liste_utilisateur.setter
    def liste_utilisateur(self, value):
        self._liste_utilisateur = value