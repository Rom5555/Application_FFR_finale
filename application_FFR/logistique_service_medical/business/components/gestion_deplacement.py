from ...data.data_deplacement import Data_deplacement
from ..entities.deplacement import Deplacement
from .ifonction_get import Ifonction_get
from .ifonction_create import Ifonction_create
from .ifonction_update import Ifonction_update


class Gestion_deplacement(Ifonction_get,Ifonction_create, Ifonction_update):

    def __init__(self):
        self.deplacement = Deplacement()
        self._data_deplacement = Data_deplacement()

    def create(self):

        self._data_deplacement.create_deplacement(self.deplacement.nombre_joueurs,self.deplacement.duree_deplacement,self.deplacement.nombre_match)

    def update(self):
        self._data_deplacement.update_deplacement(self.deplacement.nombre_joueurs,self.deplacement.duree_deplacement,self.deplacement.nombre_match)

    def get_id(self):

        row = self._data_deplacement.get_1_deplacement(self.deplacement.nombre_joueurs,self.deplacement.duree_deplacement,self.deplacement.nombre_match)
        print(row)
        return row[0]

    def get_1(self):
        row = self._data_deplacement.get_1_deplacement(self.deplacement.nombre_joueurs,
                                                       self.deplacement.duree_deplacement,
                                                       self.deplacement.nombre_match)
        print(row)
        return row

    def get_all(self):

        return self._data_deplacement.get_all_deplacement()



