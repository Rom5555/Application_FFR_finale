from django.contrib.auth.views import LoginView
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import logging
logger = logging.getLogger("django")


#Registration
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('admin_base:index')  # Rediriger l'administrateur vers la page d'administration
        else:
            return reverse_lazy('user_liste:index_utilisateur')  # Rediriger l'utilisateur standard vers une autre page après la connexion'utilisateur standard vers une autre page après la connexion


class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion après inscription
    template_name = 'registration/register.html'  #

