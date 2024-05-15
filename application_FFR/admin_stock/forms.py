from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .business.components.gestion_stock import Gestion_stock


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

