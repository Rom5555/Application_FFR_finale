
from ...data.data_liste_utilisateur import Data_liste_utilisateur
from ..entities.utilisateur import Utilisateur
from ..entities.liste_depart import Liste_depart
from ..entities.liste_utilisateur import Liste_utilisateur
from admin_stock.business.entities.produit import Produit
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


    def create(self):

        result = self._data_liste_utilisateur.create_liste_utilisateur(self.utilisateur.id, self.liste_depart.id, self.liste_utilisateur.date, self.liste_utilisateur.destination)
        return result

    def create_association_liste_utilisateur_produit(self):

        self._data_liste_utilisateur.create_association_liste_utilisateur_produit(self.liste_utilisateur.id, self.liste_depart.id)

    def get_id_liste_utilisateur_en_cours(self):

        row = self._data_liste_utilisateur.get_id_liste_utilisateur_en_cours(self.utilisateur.id)
        if row:
            print(row)
            return row[0]
        else:
            return None

    def get_1(self):

        rows = self._data_liste_utilisateur.get_liste_utilisateur(self.liste_utilisateur.id)
        for row in rows:
            print("id_liste_depart:", row[0], "id_stock:", row[1], "nom_stock:", row[2], "id_produit:", row[3],"nom_produit:", row[4], "quantite_depart:", row[5], "quantite_retour:", row[6])
        produits = []
        for row in rows:
            produit = {
                'id_produit': row[3],
                'nom_produit': row[4],
                'quantite_depart': row[5],
                'quantite_retour': row[6],
            }
            produits.append(produit)
        print(produits)
        return produits


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

    def test_liste_en_cours(self):

        return self._data_liste_utilisateur.test_liste_en_cours(self.utilisateur.id)


    def valider_liste_retour(self):
        return self._data_liste_utilisateur.valider_liste_retour(self.liste_utilisateur.id)

    def get_id_liste_archivee(self):

        rows = self._data_liste_utilisateur.get_id_liste_archivee(self.liste_depart.id)
        listes_archivees = []
        for row in rows:
            liste_archivee = {
                'id_liste_utilisateur':row[0],
                'date_liste': row[1],
                'destination': row[2],
                'en_cours': row[3],
                'id_liste_depart': row[4],
                'id_utilisateur': row[5]
            }
            listes_archivees.append(liste_archivee)
        print(listes_archivees)
        return listes_archivees

    def get_date_destination(self):

        row = self._data_liste_utilisateur.get_date_destination(self.liste_utilisateur.id)

        liste_selectionnee = {
            'id_liste_utilisateur':row[0],
            'date_liste': row[1],
            'destination': row[2],
            'en_cours': row[3],
            'id_liste_depart': row[4],
            'id_utilisateur': row[5]
            }

        print(liste_selectionnee)
        return liste_selectionnee


