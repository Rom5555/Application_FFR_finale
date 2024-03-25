from ...data.data_utilisateur import Data_utilisateur
from ...data.data_liste_utilisateur import Data_liste_utilisateur
from ..entities.utilisateur import Utilisateur
from ..entities.liste_depart import Liste_depart
from ..entities.liste_utilisateur import Liste_utilisateur
from ..entities.produit import Produit
from .ifonction_get import Ifonction_get
from .ifonction_create import Ifonction_create
from .ifonction_update import Ifonction_update


class Gestion_liste_utilisateur(Ifonction_get,Ifonction_create,Ifonction_update):



    def __init__(self):

        self.produit=Produit()
        self.utilisateur=Utilisateur()
        self.liste_depart=Liste_depart()
        self.liste_utilisateur = Liste_utilisateur()
        self._data_liste_utilisateur = Data_liste_utilisateur()
        self._data_utilisateur = Data_utilisateur()

    def create(self):

        self._data_liste_utilisateur.create_liste_utilisateur(self.utilisateur.id, self.liste_depart.id, self.liste_utilisateur.date, self.liste_utilisateur.destination)

    def create_association_liste_utilisateur_produit(self):

        self._data_liste_utilisateur.create_association_liste_utilisateur_produit(self.liste_utilisateur.id, self.liste_depart.id)

    def get_id_liste_utilisateur_en_cours(self):

        return self._data_liste_utilisateur.get_id_liste_utilisateur_en_cours(self.utilisateur.id)[0]

    def get_1(self):

        rows = self._data_liste_utilisateur.get_liste_utilisateur(self.liste_utilisateur.id)
        for row in rows:
            print("id_liste_depart:", row[0], "id_stock:", row[1], "nom_stock:", row[2], "id_produit:", row[3],"nom_produit:", row[4], "quantite_depart:", row[5], "quantite_retour:", row[6])
        return rows

    def get_all(self):

        rows = self._data_liste_utilisateur.get_all_liste_utilisateur(self.utilisateur.id)
        print(rows)
        return rows

    def get_id(self):

        return self._data_liste_utilisateur.get_id_liste_utilisateur(self.utilisateur.id,self.liste_depart.id,self.liste_utilisateur.date)[0]

    def update(self):

        self._data_liste_utilisateur.update_liste_utilisateur(self.produit.quantite_retour, self.liste_utilisateur.id, self.produit.id)

    def get_id_utilisateur(self):
        return self._data_utilisateur.get_id_utilisateur(self.utilisateur.nom,self.utilisateur.prenom)[0]