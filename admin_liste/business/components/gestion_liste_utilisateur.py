
from ...data.data_liste_utilisateur import Data_liste_utilisateur
from ..entities.utilisateur import Utilisateur
from ..entities.modele_liste import ModeleListe
from ..entities.liste_utilisateur import Liste_utilisateur
from admin_stock.business.entities.produit import Produit
from .ifonction_get import Ifonction_get
from .ifonction_create import Ifonction_create
from .ifonction_update import Ifonction_update


class GestionListeUtilisateur(Ifonction_get,Ifonction_create,Ifonction_update):



    def __init__(self):

        self.produit=Produit()
        self.utilisateur=Utilisateur()
        self.modele_liste=ModeleListe()
        self.liste_utilisateur = Liste_utilisateur()
        self._data_liste_utilisateur = Data_liste_utilisateur()


    def create(self):

        result = self._data_liste_utilisateur.create_liste_utilisateur(self.liste_utilisateur.utilisateur.id, self.liste_utilisateur.modele_liste.id, self.liste_utilisateur.equipe.id, self.liste_utilisateur.nombre_joueurs, self.liste_utilisateur.duree_deplacement, self.liste_utilisateur.nombre_match, self.liste_utilisateur.date, self.liste_utilisateur.destination)
        return result

    def create_association_liste_utilisateur_produit(self):

        self._data_liste_utilisateur.create_association_liste_utilisateur_produit(self.liste_utilisateur.id, self.liste_utilisateur.modele_liste.id)

    def get_id_liste_utilisateur_en_cours(self):

        row = self._data_liste_utilisateur.get_id_liste_utilisateur_en_cours(self.liste_utilisateur.utilisateur.id)
        if row:
            print(row)
            return row[0]
        else:
            return None

    def get_1(self):

        rows = self._data_liste_utilisateur.get_liste_utilisateur(self.liste_utilisateur.id)
        for row in rows:
            print("id_modele_liste:", row[0], "id_stock:", row[1], "nom_stock:", row[2], "id_produit:", row[3],"nom_produit:", row[4], "quantite_depart:", row[5], "quantite_retour:", row[6])
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

    def get_id_modele_liste_utilisateur(self):

        row = self._data_liste_utilisateur.get_id_modele_liste_utilisateur(self.liste_utilisateur.id)
        return row

    def get_all(self):

        rows = self._data_liste_utilisateur.get_all_liste_utilisateur(self.liste_utilisateur.utilisateur.id)
        print(rows)
        return rows

    def get_id(self):

        return self._data_liste_utilisateur.get_id_liste_utilisateur(self.liste_utilisateur.utilisateur.id,self.liste_utilisateur.modele_liste.id, self.liste_utilisateur.date)[0]

    def delete_association_liste_utilisateur_produit(self):

        self._data_liste_utilisateur.delete_association_liste_utilisateur_produit(self.liste_utilisateur.id, self.produit.id)

    def update_depart(self):

        self._data_liste_utilisateur.update_depart(self.produit.quantite_depart, self.liste_utilisateur.id, self.produit.id)

    def update(self):

        self._data_liste_utilisateur.update_retour(self.produit.quantite_retour, self.liste_utilisateur.id, self.produit.id)

    def get_id_utilisateur(self):
        return self._data_utilisateur.get_id_utilisateur(self.utilisateur.nom,self.utilisateur.prenom)[0]

    def test_liste_en_cours(self):

        return self._data_liste_utilisateur.test_liste_en_cours(self.liste_utilisateur.utilisateur.id)


    def valider_liste_retour(self):
        return self._data_liste_utilisateur.valider_liste_retour(self.liste_utilisateur.id)

    def get_listes_archivees(self):

        listes_archivees = self._data_liste_utilisateur.get_listes_archivees(self.liste_utilisateur.modele_liste.id)

        return listes_archivees

    def get_date_destination(self):

        liste_selectionnee = self._data_liste_utilisateur.get_date_destination(self.liste_utilisateur.id)

        return liste_selectionnee



    def test_association_produit_liste(self):

        return self._data_liste_utilisateur.test_association_produit_liste(self.liste_utilisateur.id, self.produit.id)
