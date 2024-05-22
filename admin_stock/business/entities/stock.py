class Stock:

    def __init__(self):
        self.id = 1
        self.nom = ""


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self,value):
        self._nom = value




