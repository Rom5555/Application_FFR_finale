

class ModeleListe:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.id = 1
        self.nom_modele_liste = ""
        self.type_rugby = 15
        self.nombre_joueurs_min = 1
        self.nombre_joueurs_max = 1
        self.duree_deplacement_min = 1
        self.duree_deplacement_max = 1
        self.nombre_match_min = 1
        self.nombre_match_max = 1

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
    def type_rugby(self):
        return self._type_rugby

    @type_rugby.setter
    def type_rugby(self,value):
        self._type_rugby = value


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
    def nombre_match_min(self):
        return self._nombre_match_min

    @nombre_match_min.setter
    def nombre_match_min(self, value):
        self._nombre_match_min = value

    @property
    def nombre_match_max(self):
        return self._nombre_match_max

    @nombre_match_max.setter
    def nombre_match_max(self, value):
        self._nombre_match_max = value


