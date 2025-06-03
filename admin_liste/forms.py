from django import forms
from django.contrib.auth.models import User
from admin_liste.business.components.gestion_equipe import GestionEquipe
from admin_liste.business.components.gestion_modele_liste import GestionModeleListe
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div


class ModeleListeForm(forms.Form):

    nom_modele_liste = forms.CharField(max_length=20, required=True, label="Nom du modèle de liste")
    type_rugby = forms.ChoiceField(choices=[], label="Type de rugby")
    genre = forms.ChoiceField(choices=[], label="Genre")
    categorie_age = forms.ChoiceField(choices=[], label="Catégorie d'âge")
    nombre_joueurs_min = forms.IntegerField(required=True, label="joueurs min")
    nombre_joueurs_max = forms.IntegerField(required=True, label="joueurs max")
    duree_deplacement_min = forms.IntegerField(required=True, label="duree min")
    duree_deplacement_max = forms.IntegerField(required=True, label="duree max")
    nombre_match = forms.IntegerField(required=True, label="matchs")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialisation des choix pour EquipeForm
        self.fields['type_rugby'].choices = self.get_type_rugby_choices()
        self.fields['genre'].choices = self.get_genre_choices()
        self.fields['categorie_age'].choices = self.get_categorie_age_choices()

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('nom_modele_liste'),
            Div(
                Div(Field('type_rugby', css_class='input'), css_class='column is-third'),
                Div(Field('genre', css_class='input'), css_class='column is-third'),
                Div(Field('categorie_age', css_class='input'), css_class='column is-third'),
                css_class='columns'
            ),
            Div(
                Div(Field('nombre_joueurs_min'), css_class='column is-half'),
                Div(Field('nombre_joueurs_max'), css_class='column is-half'),
                css_class='columns'
            ),
            Div(
                Div(Field('duree_deplacement_min'), css_class='column is-half'),
                Div(Field('duree_deplacement_max'), css_class='column is-half'),
                css_class='columns'
            ),
            Div(
                Div(Field('nombre_match'), css_class='column is-half'),
                css_class='columns'
            ),
        )
    def get_type_rugby_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_genre_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['genre'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_categorie_age_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['categorie_age'] for equipe in equipes)
        return [(value, value) for value in unique_values]


class EquipeUtilisateurForm(forms.Form):
    # Champs de EquipeForm
    type_rugby = forms.ChoiceField(choices=[], label="Type de rugby")
    genre = forms.ChoiceField(choices=[], label="Genre")
    categorie_age = forms.ChoiceField(choices=[], label="Catégorie d'âge")
    nombre_joueurs = forms.IntegerField(min_value=0, label="Nombre de joueurs")
    duree_deplacement = forms.IntegerField(min_value=0, label="Durée de déplacement")
    nombre_match = forms.IntegerField(min_value=0, label="Nombre de matchs")

    # Champs de UtilisateurChoiceForm
    utilisateur = forms.ChoiceField(choices=[], label="Utilisateur")
    date_depart = forms.DateField(label='Date de départ', required=True)
    destination = forms.CharField(label='Destination', required=True, max_length=60)

    def __init__(self, *args, **kwargs):
        super(EquipeUtilisateurForm, self).__init__(*args, **kwargs)

        # Initialisation des choix pour EquipeForm
        self.fields['type_rugby'].choices = self.get_type_rugby_choices()
        self.fields['genre'].choices = self.get_genre_choices()
        self.fields['categorie_age'].choices = self.get_categorie_age_choices()

        # Initialisation des choix pour UtilisateurChoiceForm
        utilisateurs = User.objects.all().values_list('id', 'username')
        self.fields['utilisateur'].choices = utilisateurs

        # Configuration du layout avec Crispy Forms
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('type_rugby', css_class='input'), css_class='column is-third'),
                Div(Field('genre', css_class='input'), css_class='column is-third'),
                Div(Field('categorie_age', css_class='input'), css_class='column is-third'),
                css_class='columns'
            ),

            Div(
                Div(Field('nombre_joueurs', css_class='input'), css_class='column is-third'),
                Div(Field('duree_deplacement', css_class='input'), css_class='column is-third'),
                Div(Field('nombre_match', css_class='input'), css_class='column is-third'),
                css_class='columns'
            ),

            Div( Div(Field('utilisateur', css_class='input'), css_class='column is-third'),
                Div(Field('date_depart', css_class='input'), css_class='column is-third'),
                Div(Field('destination', css_class='input'), css_class='column is-third'),
                css_class='columns'
            ),
        )

    def get_type_rugby_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_genre_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['genre'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_categorie_age_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['categorie_age'] for equipe in equipes)
        return [(value, value) for value in unique_values]

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
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_genre_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['genre'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_categorie_age_choices(self):
        gestion_equipe = GestionEquipe()
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
    type_rugby = forms.ChoiceField(choices=[], label="Type de rugby")
    nombre_joueurs = forms.ChoiceField(choices=[], label="Nombre de joueurs")
    duree_deplacement = forms.ChoiceField(choices=[], label="Durée du déplacement")
    nombre_match = forms.ChoiceField(choices=[], label="Nombre de matchs")

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(ArchiveForm, self).__init__(*args, **kwargs)
        self.fields['type_rugby'].choices = self.get_type_rugby_choices()
        self.fields['nombre_joueurs'].choices = self.get_nombre_joueurs_choices()
        self.fields['duree_deplacement'].choices = self.get_duree_deplacement_choices()
        self.fields['nombre_match'].choices = self.get_nombre_match_choices()

        self.initial['type_rugby'] = initial.get('type_rugby')
        self.initial['nombre_joueurs'] = initial.get('nombre_joueurs')
        self.initial['duree_deplacement'] = initial.get('duree_deplacement')
        self.initial['nombre_match'] = initial.get('nombre_match')

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('type_rugby'),
            Field('nombre_joueurs'),
            Field('duree_deplacement'),
            Field('nombre_match'),
        )

    def get_type_rugby_choices(self):
        gestion_equipe = GestionEquipe()
        equipes = gestion_equipe.get_all()
        unique_values = set(equipe['type_rugby'] for equipe in equipes)
        return [(value, value) for value in unique_values]

    def get_nombre_joueurs_choices(self):
        gestion_modele_liste = GestionModeleListe()
        modeles_liste = gestion_modele_liste.get_all()
        unique_values = set((modele['nombre_joueurs_min'], modele['nombre_joueurs_max']) for modele in modeles_liste)
        return [(f"{min}-{max}", f"{min} - {max} joueurs") for min, max in unique_values]

    def get_duree_deplacement_choices(self):
        gestion_modele_liste = GestionModeleListe()
        modeles_liste = gestion_modele_liste.get_all()
        unique_values = set((modele['duree_deplacement_min'], modele['duree_deplacement_max']) for modele in modeles_liste)
        return [(f"{min}-{max}", f"{min} - {max} jours") for min, max in unique_values]

    def get_nombre_match_choices(self):
        gestion_modele_liste = GestionModeleListe()
        modeles_liste = gestion_modele_liste.get_all()
        unique_values = set(modele['nombre_match'] for modele in modeles_liste)  # Correction ici
        return [(value, f"{value} matchs") for value in sorted(unique_values)]

    def clean(self):
        cleaned_data = super().clean()

        # Vérification des plages min/max
        for field in ['nombre_joueurs', 'duree_deplacement']:
            value = cleaned_data.get(field)
            if value:
                try:
                    min_val, max_val = map(int, value.split('-'))
                    if min_val >= max_val:
                        self.add_error(field, "La valeur minimale doit être inférieure à la valeur maximale.")
                except ValueError:
                    self.add_error(field, "Format invalide, attendez-vous à 'min-max'.")

        # Vérification de nombre_match
        nombre_match = cleaned_data.get('nombre_match')
        if nombre_match:
            try:
                nombre_match = int(nombre_match)
                if nombre_match <= 0:
                    self.add_error('nombre_match', "Le nombre de matchs doit être supérieur à 0.")
            except ValueError:
                self.add_error('nombre_match', "Valeur invalide pour le nombre de matchs.")

        return cleaned_data