from .gestion_stock import Gestion_stock
from ...data.data_liste_utilisateur import Data_liste_utilisateur
from ..entities.equipe import Equipe
from ..entities.liste_depart import Liste_depart
from ..entities.deplacement import Deplacement
from ..entities.produit import Produit
from ...data.data_stock import Data_stock
from ...data.data_equipe import Data_equipe
from ...data.data_deplacement import Data_deplacement
from ...data.data_liste_depart import Data_liste_depart
from .ifonction_get import Ifonction_get
from .ifonction_create import Ifonction_create
from .ifonction_update import Ifonction_update



class Gestion_liste_depart(Ifonction_get,Ifonction_create,Ifonction_update):

    def __init__(self):

        self.equipe=Equipe()
        self.deplacement=Deplacement()
        self.liste_depart=Liste_depart()
        self.produit = Produit()
        self._data_liste_depart = Data_liste_depart()
        self._data_liste_utilisateur = Data_liste_utilisateur()
        self._data_stock = Data_stock()
        self._data_equipe = Data_equipe()
        self._data_deplacement = Data_deplacement()
        self._gestion_stock = Gestion_stock()

    def create(self):

        self._data_liste_depart.create_liste_depart(self.equipe.id,self.deplacement.id)

    def create_association_liste_depart_produit(self):

        self._data_liste_depart.create_association_liste_depart_produit(self.liste_depart.id,self.produit.id, self.produit.quantite_depart)

    def update(self):

        self._data_liste_depart.update_liste_depart(self.produit.quantite_depart,self.liste_depart.id,self.produit.id)

    def get_id(self):
        row = self._data_liste_depart.get_id_liste_depart(self.equipe.id, self.deplacement.id)
        if row:
            print(row)
            return row[0]
        else:
            return None

    def get_1(self):

        rows = self._data_liste_depart.get_liste_depart(self.liste_depart.id)
        produits = []
        for row in rows:
            produit = {
                'id_liste_depart': row[0],
                'id_stock': row[1],
                'nom_stock': row[2],
                'id_produit': row[3],
                'nom_produit': row[4],
                'quantite_depart': row[5],
                'quantite_retour': row[6],
            }
            produits.append(produit)
        print(produits)
        return produits


    def test_association_produit_liste(self):

        return self._data_liste_depart.test_association_produit_liste(self.liste_depart.id, self.produit.id)

    def test_liste_exist(self):

        return self._data_liste_depart.test_exist(self.equipe.id, self.deplacement.id)

    def get_all(self):

        rows = self._data_liste_depart.get_all_liste_depart()
        for row in rows:
            print("id_liste_depart:",row[0],"type rugby",row[1],"genre",row[2],"categorie age",row[3],"nombre joueurs",row[4],"duree deplacement",row[5])

    def build_liste_depart(self):

        # verifier si la liste_depart n'existe pas déjà en testant la combinaison id_equipe,id_deplacement

        self.create()
        self.liste_depart.id = self.get_id()

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
                'id_liste_depart':0,
                'id_stock': row[0],
                'nom_stock': row[1],
                'id_produit': row[2],
                'nom_produit': row[3],
                'quantite_stock': row[4],
                'quantite_depart': 0,
                'quantite_retour': 0,
            }
            produits.append(produit)

        return produits


