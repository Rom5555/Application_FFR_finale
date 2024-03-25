from .equipe import Equipe
from .deplacement import Deplacement


class Liste_depart:
    # ------------------------------
    # constructeur
    # ------------------------------
    def __init__(self):
        self.id = 1
        self.equipe = Equipe()
        self.deplacement = Deplacement()


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
    def id_equipe(self):
        return self._id_equipe

    @id_equipe.setter
    def id_equipe(self, value):
        self._id_equipe = value

    @property
    def id_deplacement(self):
        return self._id_deplacement

    @id_deplacement.setter
    def id_deplacement(self,value):
        self._id_deplacement = value

   
