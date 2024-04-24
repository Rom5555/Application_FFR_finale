from django.forms.models import ModelChoiceField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .business.components.gestion_stock import Gestion_stock
from .business.components.gestion_equipe import Gestion_equipe
from .business.components.gestion_deplacement import Gestion_deplacement


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'S\'inscrire',css_class='button is-info'))
        self.helper.layout = Layout(
            Field('first_name', css_class='input'),
            Field('last_name', css_class='input'),
            Field('username', css_class='input'),
            Field('email', css_class='input'),
            Field('password1', css_class='input'),
            Field('password2', css_class='input'),

        )


class AddUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class DeleteUserForm(forms.Form):
    user_id = forms.IntegerField(label='ID de l\'utilisateur à supprimer')


class StockModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nom_stock




class ProduitForm(forms.Form):

    nom_produit = forms.CharField(label='Nom', max_length=60, required=True)
    quantite = forms.IntegerField(widget=forms.TextInput, label="Quantite", required=True, min_value=0)
    id_stock = forms.ChoiceField(label="Stock", required=True, choices=[])

    def __init__(self, *args, **kwargs):
        super(ProduitForm, self).__init__(*args, **kwargs)
        gestion_stock = Gestion_stock()
        stocks = gestion_stock.get_all()
        choices = [(stock['id_stock'], stock['nom_stock']) for stock in stocks]
        self.fields['id_stock'].choices = [("", "(Choisir un stock)")] + choices



class ProductQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        initial=1,
        label='',
        widget=forms.NumberInput(attrs={'placeholder': ''}),
        required=False, min_value="0"  # Rendre le champ facultatif pour éviter le message "Ce champ est obligatoire"
    )

    def __init__(self, *args, **kwargs):
        super(ProductQuantityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False  # Désactiver l'affichage des étiquettes
        self.helper.layout = Layout(
            Field('quantity', css_class='input is-small', aria_describedby=""),
            Submit('submit', 'Ajouter', css_class='button is-primary is-small')
        )


class DeleteProduitForm(forms.Form):
    id_produit = forms.IntegerField(label='ID du produit à supprimer')




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
