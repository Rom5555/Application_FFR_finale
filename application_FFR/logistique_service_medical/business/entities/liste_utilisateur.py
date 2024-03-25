from datetime import date
from .utilisateur import Utilisateur
from .liste_depart import Liste_depart


class Liste_utilisateur:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):

        self.id = 1
        self.utilisateur = Utilisateur()
        self.liste_depart = Liste_depart()
        self.destination = ""
        self.date = date(2024,1,22)
        self.en_cours = True

    # ------------------------------
    # propriétés
    # ------------------------------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


    @property
    def utilisateur(self):
        return self._utilisateur

    @utilisateur.setter
    def utilisateur(self, value):
        self._utilisateur = value

    @property
    def liste_depart(self):
        return self._liste_depart

    @liste_depart.setter
    def liste_depart(self,value):
        self._liste_depart = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def en_cours(self):
        return self._en_cours

    @en_cours.setter
    def en_cours(self, value):
        self._en_cours = value

   
