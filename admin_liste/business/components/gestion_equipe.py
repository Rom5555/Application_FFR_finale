from ...data.data_equipe import Data_equipe
from ..entities.equipe import Equipe
from .ifonction_get import Ifonction_get


class Gestion_equipe(Ifonction_get):

    def __init__(self):
        self.equipe = Equipe()
        self._data_equipe = Data_equipe()

    def get_id(self):

        row = self._data_equipe.get_1_equipe(self.equipe.type_rugby,self.equipe.genre, self.equipe.categorie_age)
        print(row)
        return row[0]

    def get_1(self):
        row = self._data_equipe.get_1_equipe(self.equipe.type_rugby, self.equipe.genre, self.equipe.categorie_age)
        print(row)
        return row

    def get_all(self):
        rows = self._data_equipe.get_all_equipe()
        equipes = []
        for row in rows:
            equipe={
                'id': row[0],
                'type_rugby': row[1],
                'genre': row[2],
                'categorie_age': row[3],
            }
            equipes.append(equipe)
        print(equipes)
        return equipes

