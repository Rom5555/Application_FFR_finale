from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Stock, Produit, AssociationStockProduit
from django.contrib.auth.decorators import login_required
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import logging
from django.contrib.auth.models import User
from .business.components.gestion_stock import Gestion_stock
from .business.components.gestion_equipe import Gestion_equipe
from .business.components.gestion_deplacement import Gestion_deplacement
from .business.components.gestion_liste_depart import Gestion_liste_depart
logger = logging.getLogger("django")

class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion après inscription
    template_name = 'registration/register.html'  #


# views.py
def user_list(request):
    users = User.objects.all()
    add_user_form = RegisterForm()
    delete_user_form = DeleteUserForm()
    return render(request, 'logistique_service_medical/user_list.html',
                  {'users': users, 'add_user_form': add_user_form, 'delete_user_form': delete_user_form})




from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import RegisterForm

class AddUserView(SuccessMessageMixin, CreateView):
    template_name = 'logistique_service_medical/user_list.html'
    form_class = RegisterForm
    success_url = reverse_lazy('logistique_service_medical:user_list')
    success_message = "Utilisateur ajouté avec succès."


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_user_form'] = self.get_form()  # Ajouter le formulaire au contexte
        return context


def delete_user(request):
    if request.method == 'POST':
        delete_user_form = DeleteUserForm(request.POST)
        if delete_user_form.is_valid():
            user_id = delete_user_form.cleaned_data['user_id']
            user_to_delete = User.objects.filter(id=user_id).first()
            if user_to_delete:
                user_to_delete.delete()
    return redirect('logistique_service_medical:user_list')

@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def index(request):
    logger.debug("entrée dans la view 'Index'")
    template = loader.get_template('logistique_service_medical/index.html')
    context={}
    logger.warning('le contexte pour la view est vide')

    logger.info(f"Définition des villes favorites pour l'utilisateur")
    liste_villes_favorites = ['Paris', 'Lyon', 'Strasbourg']
    request.session['favoris'] = liste_villes_favorites

    logger.debug("sortie dans la view 'Index', rendu du tempate...")

    return HttpResponse(template.render(context, request))

gestion_stock = Gestion_stock()

@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def stock_consommables(request):
    consommables = gestion_stock.get_1()
    context = {'consommables': consommables}
    return render(request, 'logistique_service_medical/stock_consommables.html', context)


@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def select_stock(request):
    liste_stocks = gestion_stock.get_all()  # Utilise la méthode get_all de Gestion_stock
    context = {
        'liste_stocks': liste_stocks,
    }
    return render(request, 'logistique_service_medical/select_stock.html', context)


@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def display_produits(request):
    liste_stocks = gestion_stock.get_all()
    produitsStock = None
    selected_stock_id = ''
    selected_stock_nom = ''

    if request.method == 'POST':
        id_stock = request.POST.get('id_stock')
        if id_stock:
            gestion_stock.stock.id = id_stock
            produitsStock = gestion_stock.get_1()
            selected_stock_id = id_stock
            selected_stock_nom = produitsStock[0]['nom_stock']

    form = ProductQuantityForm()
    context = {
        'produitsStock': produitsStock,
        'liste_stocks': liste_stocks,
        'selected_stock_id': selected_stock_id,
        'selected_stock_nom': selected_stock_nom,
        'form': form,
    }
    return render(request, 'logistique_service_medical/display_produits.html', context)


@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def update_quantity(request, id_produit):
    if request.method == 'POST':
        if id_produit:
            new_quantity_key = f'quantity_{id_produit}'
            new_quantity = request.POST.get(new_quantity_key)
            if new_quantity is not None:
                try:
                    gestion_stock.produit.id = id_produit
                    gestion_stock.produit.quantite_en_stock = int(new_quantity)
                    gestion_stock.update_quantity()  # Utilise la méthode update_quantity de Gestion_stock
                    response_message = 'Quantité mise à jour avec succès'
                    return HttpResponse(response_message, status=200)
                except Exception as e:
                    return HttpResponse('Erreur lors de la mise à jour de la quantité', status=400)
            else:
                return HttpResponse('Aucune quantité spécifiée dans la requête', status=400)
        else:
            return HttpResponse('Aucun ID d\'association de stock-produit spécifié dans la requête', status=400)
    return HttpResponse('Méthode de requête invalide', status=405)


from django.contrib import messages

def produit_list(request):
    produits = gestion_stock.get_all_produit()
    add_produit_form = ProduitForm()
    delete_produit_form = DeleteProduitForm()

    # Récupérer le message de succès de la session s'il existe
    success_message = None
    if 'success_message' in request.session:
        success_message = request.session['success_message']
        del request.session['success_message']  # Supprimer le message de la session

    return render(request, 'logistique_service_medical/produit_list.html',
                  {'produits': produits, 'add_produit_form': add_produit_form,
                   'delete_produit_form': delete_produit_form, 'success_message': success_message})


@login_required(login_url='/logistique_service_medical/login/')
def add_produit(request):
    save_error = False
    is_create = True
    add_produit_form = ProduitForm()

    if request.method == 'POST':
        is_create = False
        add_produit_form = ProduitForm(request.POST)

        if add_produit_form.is_valid():
            nom_produit = add_produit_form.cleaned_data["nom_produit"]
            quantite = add_produit_form.cleaned_data["quantite"]
            id_stock = add_produit_form.cleaned_data["id_stock"]

            try:
                gestion_stock.produit.nom = nom_produit
                gestion_stock.produit.quantite_en_stock = quantite
                gestion_stock.stock.id = id_stock

                # Afficher les valeurs récupérées dans la console
                print("Nom du produit:", nom_produit)
                print("Quantité:", quantite)
                print("ID du stock:", id_stock)

                gestion_stock.add_produit_stock()
                add_produit_form = ProduitForm()

                # Stocker le message de succès dans la session
                messages.success(request, 'Le produit a été ajouté avec succès.')

                # Rediriger vers la liste des produits
                return redirect('logistique_service_medical:produit_list')

            except Exception as e:
                print(e)
                save_error = True

    # Si l'ajout du produit a échoué, ne pas stocker de message de succès dans la session
    if save_error:
        messages.error(request, 'Erreur lors de l\'ajout du produit.')

    return render(request, 'logistique_service_medical/produit_list.html',
                  {'add_produit_form': add_produit_form, 'save_error': save_error, 'is_create': is_create})

@login_required(login_url='/logistique_service_medical/login/')
def delete_produit(request):
    if request.method == 'POST':
        delete_produit_form = DeleteProduitForm(request.POST)
        if delete_produit_form.is_valid():
            id_produit = delete_produit_form.cleaned_data['id_produit']
            try:
                gestion_stock.produit.id = id_produit
                gestion_stock.delete_produit_stock()  # Utilise la méthode delete_produit_stock de Gestion_stock
                messages.success(request, 'Le produit a été supprimé avec succès.')
            except Exception as e:
                messages.error(request, 'Erreur lors de la suppression du produit.')
    return redirect('logistique_service_medical:produit_list')


@login_required(login_url=f'/logistique_service_medical/login/?next=/logistique_service_medical/login/')
def favoris(request):
    liste_villes_favorites = ['Paris', 'Lyon', 'Strasbourg']
    request.session['favoris'] = liste_villes_favorites
    context = {'favoris': liste_villes_favorites}
    return render(request, 'logistique_service_medical/favoris.html', context)


  # Adapter cet import en fonction de la structure de votre projet

def liste_depart(request):
    # Initialisation de vos classes métier
    gestion_equipe = Gestion_equipe()
    gestion_deplacement = Gestion_deplacement()
    gestion_liste_depart = Gestion_liste_depart()
    produits_stock = []
    produits_liste = []
    id_liste_depart=0

    # Récupération de toutes les équipes en utilisant la méthode get_all() de votre classe métier
    equipes = gestion_equipe.get_all()

    # Si le formulaire est soumis (méthode POST)
    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données soumises par l'utilisateur
        equipe_form = EquipeForm(request.POST)
        # Vérification si le formulaire est valide
        if equipe_form.is_valid():

            #1-choisir une équipe pour recuperer un id_equipe

            gestion_equipe.equipe.type_rugby = equipe_form.cleaned_data['type_rugby']
            gestion_equipe.equipe.genre = equipe_form.cleaned_data['genre']
            gestion_equipe.equipe.categorie_age = equipe_form.cleaned_data['categorie_age']

            gestion_liste_depart.equipe.id = gestion_equipe.get_id()
            print(gestion_liste_depart.equipe.id)

            # 2-creer un deplacement pour recuperer un id_deplacement si il existe déjà, reprendre l'id_existant.

            gestion_deplacement.deplacement.nombre_joueurs = equipe_form.cleaned_data['nombre_joueurs']
            gestion_deplacement.deplacement.duree_deplacement = equipe_form.cleaned_data['duree_deplacement']
            gestion_deplacement.deplacement.nombre_match = equipe_form.cleaned_data['nombre_match']

            gestion_deplacement.create()
            gestion_liste_depart.deplacement.id = gestion_deplacement.get_id()
            print(gestion_liste_depart.deplacement.id)

            # 3-verifier si la liste_depart n'existe pas déjà en testant la combinaison id_equipe,id_deplacement

            if gestion_liste_depart.get_id() is None:

                gestion_liste_depart.create()
                print("Liste creee")

            gestion_liste_depart.liste_depart.id = gestion_liste_depart.get_id()
            produits_liste = gestion_liste_depart.get_1()
            print(produits_liste)
            id_liste_depart = gestion_liste_depart.liste_depart.id

            produits_stock = gestion_liste_depart.get_liste_vierge()

            for produit_stock in produits_stock:
                for produit_liste in produits_liste:
                    if produit_stock['id_produit'] == produit_liste['id_produit']:
                        produit_stock['quantite_depart'] = produit_liste['quantite_depart']
                        produit_stock['quantite_retour'] = produit_liste['quantite_retour']
                        break


    else:
        # Création d'une instance du formulaire vide
        equipe_form = EquipeForm()


    context = {'equipes': equipes, 'equipe_form': equipe_form,'produits_stock' : produits_stock, 'produits_liste' : produits_liste, 'id_liste_depart': id_liste_depart }

    # Affichage de la page avec le formulaire
    return render(request, 'logistique_service_medical/liste_depart.html', context)


def remplir_liste_depart(request, id_liste_depart, id_produit):
    gestion_liste_depart = Gestion_liste_depart()
    if request.method == 'POST':
        if id_produit:
            quantite_depart_key = f'quantity_{id_produit}'
            quantite_depart = request.POST.get(quantite_depart_key)
            if quantite_depart is not None:
                try:
                    gestion_liste_depart.liste_depart.id = id_liste_depart
                    gestion_liste_depart.produit.id = id_produit
                    gestion_liste_depart.produit.quantite_depart = int(quantite_depart)

                    if gestion_liste_depart.test_association_produit_liste():
                        gestion_liste_depart.update()
                        response_message = 'Quantité mise à jour avec succès'
                        return HttpResponse(response_message, status=200)

                    else:
                        gestion_liste_depart.create_association_liste_depart_produit()  # Utilise la méthode update_quantity de Gestion_stock
                        response_message = 'Quantité mise à jour avec succès'
                        return HttpResponse(response_message, status=200)

                except Exception as e:
                    return HttpResponse('Erreur lors de la mise à jour de la quantité', status=400)
            else:
                return HttpResponse('Aucune quantité spécifiée dans la requête', status=400)
        else:
            return HttpResponse('Aucun ID d\'association de stock-produit spécifié dans la requête', status=400)
    return HttpResponse('Méthode de requête invalide', status=405)




