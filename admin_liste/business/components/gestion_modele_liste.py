from admin_stock.business.components.gestion_stock import Gestion_stock
from ...data.data_liste_utilisateur import Data_liste_utilisateur
from ..entities.equipe import Equipe
from ..entities.modele_liste import ModeleListe
from admin_stock.business.entities.produit import Produit
from admin_stock.data.data_stock import Data_stock
from ...data.data_equipe import Data_equipe
from ...data.data_deplacement import Data_deplacement
from ...data.data_modele_liste import DataModeleListe
from .ifonction_get import Ifonction_get
from .ifonction_create import Ifonction_create
from .ifonction_update import Ifonction_update



class GestionModeleListe(Ifonction_get,Ifonction_create,Ifonction_update):

    def __init__(self):

        self.modele_liste = ModeleListe()
        self.produit = Produit()
        self._data_modele_liste = DataModeleListe()
        self._data_liste_utilisateur = Data_liste_utilisateur()
        self._data_stock = Data_stock()
        self._data_equipe = Data_equipe()
        self._data_deplacement = Data_deplacement()
        self._gestion_stock = Gestion_stock()

    def create(self):

        self._data_modele_liste.create_modele_liste(self.modele_liste.nom_modele_liste, self.modele_liste.equipe.id, self.modele_liste.nombre_joueurs_min, self.modele_liste.nombre_joueurs_max,self.modele_liste.duree_deplacement_min, self.modele_liste.duree_deplacement_max,self.modele_liste.nombre_match)

    def create_association_modele_liste_produit(self):

        if int(self.produit.quantite_depart) > 0:
            self._data_modele_liste.create_association_modele_liste_produit(self.modele_liste.id, self.produit.id, self.produit.quantite_depart)

        else:
            print("la quantite_depart du produit est egale à 0")

    def delete_association_modele_liste_produit(self):

        self._data_modele_liste.delete_association_modele_liste_produit(self.modele_liste.id, self.produit.id)

    def update(self):

        self._data_modele_liste.update_modele_liste(self.produit.quantite_depart,self.modele_liste.id,self.produit.id)

    def get_id(self):
        row = self._data_modele_liste.get_id_modele_liste(self.modele_liste.nom_modele_liste)
        if row:
            print(row)
            return row[0]
        else:
            return None

    def get_id_multiples_parametres(self):
        row = self._data_modele_liste.get_id_multiples_parametres(self.modele_liste.equipe.id, self.modele_liste.nombre_joueurs_min,self.modele_liste.nombre_joueurs_max, self.modele_liste.duree_deplacement_min, self.modele_liste.duree_deplacement_max, self.modele_liste.nombre_match)
        if row:
            print(row)
            return row[0]
        else:
            return None


    def get_1(self):

        rows = self._data_modele_liste.get_modele_liste(self.modele_liste.id)
        produits = []
        for row in rows:
            produit = {
                'id_modele_liste': row[0],
                'id_stock': row[1],
                'nom_stock': row[2],
                'id_produit': row[3],
                'nom_produit': row[4],
                'quantite_depart': row[5],
                'quantite_retour': row[6],
            }
            produits.append(produit)

        return produits


    def test_association_produit_liste(self):

        return self._data_modele_liste.test_association_produit_liste(self.modele_liste.id, self.produit.id)

    def test_modele_liste_exist(self):

        return self._data_modele_liste.test_exist(self.modele_liste.id)

    def get_all(self):

        modeles_listes = self._data_modele_liste.get_all_modele_liste()
        
        return modeles_listes

    def build_modele_liste(self):

        # verifier si la liste_depart n'existe pas déjà en testant la combinaison id_equipe,id_deplacement

        self.create()
        self.modele_liste.id = self.get_id()

        # remplir la liste_depart de produits si elle n'existe pas
        liste = []
        stocks = self._gestion_stock.get_all()
        for stock in stocks:
            self._gestion_stock.stock.id = stock['id_stock']
            produits = self._gestion_stock.get_1()
            liste.append(produits)

        print(liste)
        return liste

    def get_liste_vierge(self):

        rows = self._data_stock.get_all_stocks_produits()
        produits = []
        for row in rows:
            produit={
                'id_modele_liste': 0,
                'id_stock': row[0],
                'nom_stock': row[1],
                'id_produit': row[2],
                'nom_produit': row[3],
                'quantite_stock': row[4],
                'quantite_depart': None,
                'quantite_retour': None,
            }
            produits.append(produit)

        return produits


