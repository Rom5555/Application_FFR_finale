from django.contrib.auth.decorators import user_passes_test
from registration.permissions import is_admin, is_standard_user
from django.shortcuts import render,redirect
from registration.forms import RegisterForm
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import logging
from django.contrib.auth.models import User
logger = logging.getLogger("django")

#Gestion comptes
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    add_user_form = RegisterForm()
    delete_user_form = DeleteUserForm()
    return render(request, 'user_list.html',
                  {'users': users, 'add_user_form': add_user_form, 'delete_user_form': delete_user_form})


class AddUserView(SuccessMessageMixin, CreateView):
    template_name = 'user_list.html'
    form_class = RegisterForm
    success_url = reverse_lazy('admin_compte:user_list')
    success_message = "Utilisateur ajouté avec succès."


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_user_form'] = self.get_form()  # Ajouter le formulaire au contexte
        return context

@user_passes_test(is_admin)
def delete_user(request):
    if request.method == 'POST':
        delete_user_form = DeleteUserForm(request.POST)
        if delete_user_form.is_valid():
            user_id = delete_user_form.cleaned_data['user_id']
            user_to_delete = User.objects.filter(id=user_id).first()
            if user_to_delete:
                user_to_delete.delete()
    return redirect('admin_compte:user_list')

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion après inscription
    template_name = 'register.html'  #