from application_FFR.logistique_service_medical.data.data_utilisateur import Data_utilisateur
from application_FFR.logistique_service_medical.business.entities.utilisateur import Utilisateur
from application_FFR.logistique_service_medical.business.components.ifonction_get import Ifonction_get
from application_FFR.logistique_service_medical.business.components.ifonction_create import Ifonction_create
from application_FFR.logistique_service_medical.business.components.ifonction_update import Ifonction_update


class Gestion_compte(Ifonction_get,Ifonction_create, Ifonction_update):

    def __init__(self):

        self.utilisateur = Utilisateur()
        self._data_utilisateur = Data_utilisateur()

    def verifier_identifiant(self):

        try:
            row = self._data_utilisateur.get_1_utilisateur(self.utilisateur.mail, self.utilisateur.mot_de_passe)
            self.utilisateur.nom = row[1]
            self.utilisateur.prenom = row[2]
            self.utilisateur.mail = row[3]
            self.utilisateur.mot_de_passe = row[4]
            self.utilisateur.is_admin = row[5]
            print("Bonjour", self.utilisateur.nom, self.utilisateur.prenom)
            print("Type utilisateur: administrateur" if self.utilisateur.is_admin else "Type utilisateur: normal")
            if self.utilisateur.is_admin:
                return True


        except Exception as e:
            print(f"Erreur : {e}")
            print("Les identifiants sont introuvables")

    def create(self):

        self._data_utilisateur.create_compte_utilisateur(self.utilisateur.nom, self.utilisateur.prenom,
                                                         self.utilisateur.mail, self.utilisateur.mot_de_passe)

    def get_all(self):
        return self._data_utilisateur.get_all_utilisateur()

    def get_1(self):
        return self._data_utilisateur.get_1_utilisateur(self.utilisateur.mail, self.utilisateur.mot_de_passe)

    def get_id(self):
        return self._data_utilisateur.get_id_utilisateur(self.utilisateur.nom,self.utilisateur.prenom)[0]

    def update(self):
        self._data_utilisateur.update_compte_utilisateur(self.utilisateur.nom,self.utilisateur.prenom,self.utilisateur.mail,self.utilisateur.mot_de_passe)

    def delete_1_utilisateur(self):
        self._data_utilisateur.delete_1_utilisateur(self.utilisateur.id)

