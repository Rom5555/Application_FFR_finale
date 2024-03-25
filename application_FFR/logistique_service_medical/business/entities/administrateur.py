from .utilisateur import Utilisateur

class Administrateur(Utilisateur):

    def __init__(self):

        self._is_admin = True
        super().__init__()







