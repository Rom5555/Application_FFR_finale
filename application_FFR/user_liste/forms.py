from django.forms.models import ModelChoiceField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .business.components.gestion_stock import Gestion_stock
from .business.components.gestion_equipe import Gestion_equipe
from .business.components.gestion_deplacement import Gestion_deplacement
