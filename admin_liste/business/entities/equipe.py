class Equipe:

    def __init__(self):

        self.id = 1
        self.type_rugby = ""
        self.genre = ""
        self.categorie_age = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def type_rugby(self):
        return self._type_rugby

    @type_rugby.setter
    def type_rugby(self,value):
        self._type_rugby = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre (self,value):
        self._genre = value

    @property
    def categorie_age(self):
        return self._categorie_age

    @categorie_age.setter
    def categorie_age(self,value):
        self._categorie_age = value



