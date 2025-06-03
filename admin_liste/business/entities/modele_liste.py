from .equipe import Equipe

class ModeleListe:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.id = 1
        self.nom_modele_liste = ""
        self.equipe = Equipe()
        self.nombre_joueurs_min = 1
        self.nombre_joueurs_max = 1
        self.duree_deplacement_min = 1
        self.duree_deplacement_max = 1
        self.nombre_match = 1


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
    def nom_modele_liste(self):
        return self._nom_modele_liste

    @nom_modele_liste.setter
    def nom_modele_liste(self, value):
        self._nom_modele_liste = value

    @property
    def equipe(self):
        return self._equipe

    @equipe.setter
    def equipe(self,value):
        self._equipe = value


    @property
    def nombre_joueurs_min(self):
        return self._nombre_joueurs_min

    @nombre_joueurs_min.setter
    def nombre_joueurs_min(self, value):
        self._nombre_joueurs_min = value

    @property
    def nombre_joueurs_max(self):
        return self._nombre_joueurs_max

    @nombre_joueurs_max.setter
    def nombre_joueurs_max(self, value):
        self._nombre_joueurs_max = value

    @property
    def duree_deplacement_min(self):
        return self._duree_deplacement_min

    @duree_deplacement_min.setter
    def duree_deplacement_min(self, value):
        self._duree_deplacement_min = value

    @property
    def duree_deplacement_max(self):
        return self._duree_deplacement_max

    @duree_deplacement_max.setter
    def duree_deplacement_max(self, value):
        self._duree_deplacement_max = value

    @property
    def nombre_match(self):
        return self._nombre_match

    @nombre_match.setter
    def nombre_match(self, value):
        self._nombre_match = value



