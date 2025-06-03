from datetime import date
from .utilisateur import Utilisateur
from .modele_liste import ModeleListe
from .equipe import Equipe


class Liste_utilisateur:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):

        self.id = 1
        self.utilisateur = Utilisateur()
        self.modele_liste = ModeleListe()
        self.equipe = Equipe()
        self.nombre_joueurs = 1
        self.duree_deplacement = 1
        self.nombre_match = 1
        self.destination = ""
        self.date = date(2024,1,22)
        self.statut = None

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
    def modele_liste(self):
        return self._modele_liste

    @modele_liste.setter
    def modele_liste(self,value):
        self._modele_liste = value

    @property
    def equipe(self):
        return self._equipe

    @equipe.setter
    def equipe(self, value):
        self._equipe = value


    @property
    def nombre_joueurs(self):
        return self._nombre_joueurs

    @nombre_joueurs.setter
    def nombre_joueurs(self, value):
        self._nombre_joueurs = value


    @property
    def duree_deplacement(self):
        return self._duree_deplacement

    @duree_deplacement.setter
    def duree_deplacement(self, value):
        self._duree_deplacement = value


    @property
    def nombre_match(self):
        return self._nombre_match

    @nombre_match.setter
    def nombre_match(self, value):
        self._nombre_match = value



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
    def statut(self):
        return self._statut

    @statut.setter
    def statut(self, value):
        self._statut = value

   
