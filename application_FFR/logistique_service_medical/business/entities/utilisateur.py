class Utilisateur:

    def __init__(self):

        self.id = 1
        self.nom = ""
        self.prenom = ""
        self.mail = ""
        self.mot_de_passe = ""
        self._is_admin = "False"

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

    @property
    def prenom(self):
        return self._prenom

    @prenom.setter
    def prenom(self,value):
        self._prenom = value


    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self,value):
        self._mail = value

    @property
    def mot_de_passe(self):
        return self._mot_de_passe

    @mot_de_passe.setter
    def mot_de_passe(self, value):
        self._mot_de_passe = value

