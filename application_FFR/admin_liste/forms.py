from django import forms
from django.contrib.auth.models import User
from admin_liste.business.components.gestion_equipe import Gestion_equipe
from admin_liste.business.components.gestion_deplacement import Gestion_deplacement


class EquipeForm(forms.Form):

    type_rugby = forms.ChoiceField(choices=[])
    genre = forms.ChoiceField(choices=[])
    categorie_age = forms.ChoiceField(choices=[])
    nombre_joueurs = forms.IntegerField(min_value=0)
    duree_deplacement = forms.IntegerField(min_value=0)
    nombre_match = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        super(EquipeForm, self).__init__(*args, **kwargs)
        self.fields['type_rugby'].choices = self.get_type_rugby_choices()
        self.fields['genre'].choices = self.get_genre_choices()
        self.fields['categorie_age'].choices = self.get_categorie_age_choices()

    def get_type_rugby_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_genre_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['genre'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_categorie_age_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['categorie_age'] for equipe in equipes)
        return [(value, value) for value in unique_values]

class UtilisateurChoiceForm(forms.Form):
    utilisateur = forms.ChoiceField(choices=[])
    date_depart = forms.DateField(label='date_depart', required=True)
    destination = forms.CharField(label='destination', required=True, max_length=60)

    def __init__(self, *args, **kwargs):
        super(UtilisateurChoiceForm, self).__init__(*args, **kwargs)
        # Récupérer la liste des utilisateurs depuis la base de données
        utilisateurs = User.objects.all().values_list('id', 'username')  # username est le nom d'utilisateur par défaut de Django
        # Mettre à jour les choix du ChoiceField
        self.fields['utilisateur'].choices = utilisateurs

class ListeUtilisateurForm(forms.Form):
    utilisateur = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(ListeUtilisateurForm, self).__init__(*args, **kwargs)
        # Récupérer la liste des utilisateurs depuis la base de données
        utilisateurs = User.objects.all().values_list('id', 'username')  # username est le nom d'utilisateur par défaut de Django
        # Mettre à jour les choix du ChoiceField
        self.fields['utilisateur'].choices = utilisateurs




class ArchiveForm(forms.Form):
    type_rugby = forms.ChoiceField(choices=[])
    genre = forms.ChoiceField(choices=[])
    categorie_age = forms.ChoiceField(choices=[])
    nombre_joueurs = forms.ChoiceField(choices=[])
    duree_deplacement = forms.ChoiceField(choices=[])
    nombre_match = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(ArchiveForm, self).__init__(*args, **kwargs)
        self.fields['type_rugby'].choices = self.get_type_rugby_choices()
        self.fields['genre'].choices = self.get_genre_choices()
        self.fields['categorie_age'].choices = self.get_categorie_age_choices()
        self.fields['nombre_joueurs'].choices = self.get_nombre_joueurs_choices()
        self.fields['duree_deplacement'].choices = self.get_duree_deplacement_choices()
        self.fields['nombre_match'].choices = self.get_nombre_match_choices()

        self.initial['type_rugby'] = initial.get('type_rugby')
        self.initial['genre'] = initial.get('genre')
        self.initial['categorie_age'] = initial.get('categorie_age')
        self.initial['nombre_joueurs'] = initial.get('nombre_joueurs')
        self.initial['duree_deplacement'] = initial.get('duree_deplacement')
        self.initial['nombre_match'] = initial.get('nombre_match')

    def get_type_rugby_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_genre_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['genre'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_categorie_age_choices(self):
        gestion_equipe = Gestion_equipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['categorie_age'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_nombre_joueurs_choices(self):
        gestion_deplacement = Gestion_deplacement()
        deplacements = gestion_deplacement.get_all()
        unique_values = set(deplacement['nombre_joueurs'] for deplacement in deplacements)
        return [(value, value) for value in unique_values]

    def get_duree_deplacement_choices(self):
        gestion_deplacement = Gestion_deplacement()
        deplacements = gestion_deplacement.get_all()
        unique_values = set(deplacement['duree_deplacement'] for deplacement in deplacements)
        return [(value, value) for value in unique_values]

    def get_nombre_match_choices(self):
        gestion_deplacement = Gestion_deplacement()
        deplacements = gestion_deplacement.get_all()
        unique_values = set(deplacement['nombre_match'] for deplacement in deplacements)
        return [(value, value) for value in unique_values]
