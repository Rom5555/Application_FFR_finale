from django.forms.models import ModelChoiceField
from django import forms
from django.contrib.auth.models import User


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

