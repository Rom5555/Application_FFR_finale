from django.contrib.auth.decorators import user_passes_test
from .permissions import is_admin, is_standard_user
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from django.template import loader
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
import logging
from django.contrib.auth.models import User
from .business.components.gestion_stock import Gestion_stock
from .business.components.gestion_equipe import Gestion_equipe
from .business.components.gestion_deplacement import Gestion_deplacement
from .business.components.gestion_liste_depart import Gestion_liste_depart
from .business.components.gestion_liste_utilisateur import Gestion_liste_utilisateur
logger = logging.getLogger("django")




class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return 'logistique_service_medical/index'  # Rediriger l'administrateur vers la page d'administration
        else:
            return 'logistique_service_medical/index_utilisateur'  # Rediriger l'utilisateur standard vers une autre page après la connexion


# Gestion utilisateur
class RegisterView(CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # Redirection vers la page de connexion après inscription
    template_name = 'registration/register.html'  #


@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    add_user_form = RegisterForm()
    delete_user_form = DeleteUserForm()
    return render(request, 'logistique_service_medical/user_list.html',
                  {'users': users, 'add_user_form': add_user_form, 'delete_user_form': delete_user_form})


class AddUserView(SuccessMessageMixin, CreateView):
    template_name = 'logistique_service_medical/user_list.html'
    form_class = RegisterForm
    success_url = reverse_lazy('logistique_service_medical:user_list')
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
    return redirect('logistique_service_medical:user_list')

# Page acceuil
@user_passes_test(is_admin)
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

# Gestion stock

@user_passes_test(is_admin)
def stock_consommables(request):
    gestion_stock = Gestion_stock()
    consommables = gestion_stock.get_1()
    context = {'consommables': consommables}
    return render(request, 'logistique_service_medical/stock_consommables.html', context)

@user_passes_test(is_admin)
def select_stock(request):
    gestion_stock = Gestion_stock()
    liste_stocks = gestion_stock.get_all()  # Utilise la méthode get_all de Gestion_stock
    context = {
        'liste_stocks': liste_stocks,
    }
    return render(request, 'logistique_service_medical/select_stock.html', context)


@user_passes_test(is_admin)
def display_produits(request):
    gestion_stock = Gestion_stock()
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


@user_passes_test(is_admin)
def update_quantity(request, id_produit):
    gestion_stock = Gestion_stock()
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


@user_passes_test(is_admin)
def produit_list(request):
    gestion_stock=Gestion_stock()
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


@user_passes_test(is_admin)
def add_produit(request):
    gestion_stock= Gestion_stock()
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

@user_passes_test(is_admin)
def delete_produit(request):
    gestion_stock=Gestion_stock()
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

@user_passes_test(is_admin)
def favoris(request):
    liste_villes_favorites = ['Paris', 'Lyon', 'Strasbourg']
    request.session['favoris'] = liste_villes_favorites
    context = {'favoris': liste_villes_favorites}
    return render(request, 'logistique_service_medical/favoris.html', context)


#Gestion Liste

@user_passes_test(is_admin)
def depart_retour(request):

    template = loader.get_template('logistique_service_medical/depart_retour.html')
    context = {}
    return HttpResponse(template.render(context, request))


# Preparer un depart

@user_passes_test(is_admin)
def depart(request):
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

    utilisateur_choice_form = UtilisateurChoiceForm()

    context = {'equipes': equipes, 'equipe_form': equipe_form,'produits_stock': produits_stock, 'produits_liste': produits_liste, 'id_liste_depart': id_liste_depart, 'utilisateur_choice_form': utilisateur_choice_form}

    # Affichage de la page avec le formulaire
    return render(request, 'logistique_service_medical/depart.html', context)

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def create_liste_utilisateur(request, id_liste_depart):

    gestion_stock = Gestion_stock()
    gestion_liste_utilisateur = Gestion_liste_utilisateur()

    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données soumises par l'utilisateur
        utilisateur_choice_form = UtilisateurChoiceForm(request.POST)

        # Vérification si le formulaire est valide
        if utilisateur_choice_form.is_valid():
            # Récupération des données du formulaire
            id_utilisateur = utilisateur_choice_form.cleaned_data['utilisateur']
            date_depart = utilisateur_choice_form.cleaned_data['date_depart']
            destination = utilisateur_choice_form.cleaned_data['destination']


            # Création de la liste utilisateur pour le depart avec les 4 paramètres

            try:
                gestion_liste_utilisateur.liste_depart.id = id_liste_depart
                print(gestion_liste_utilisateur.liste_depart.id)
                gestion_liste_utilisateur.utilisateur.id = int(id_utilisateur)
                print(gestion_liste_utilisateur.utilisateur.id)
                gestion_liste_utilisateur.liste_utilisateur.date = date_depart
                print(gestion_liste_utilisateur.liste_utilisateur.date)
                gestion_liste_utilisateur.liste_utilisateur.destination = destination
                print(gestion_liste_utilisateur.liste_utilisateur.destination)

                if gestion_liste_utilisateur.test_liste_en_cours():

                    print("Une liste est deja en cours pour cet utilisateur")

                else:

                    gestion_liste_utilisateur.create()
                    gestion_liste_utilisateur.liste_utilisateur.id = gestion_liste_utilisateur.get_id()
                    # Remplissage de la liste utilisateur
                    gestion_liste_utilisateur.create_association_liste_utilisateur_produit()
                    gestion_liste_utilisateur.get_1()

                    produits_liste_utilisateur=gestion_liste_utilisateur.get_1()
                    print("La liste utilisateur:", produits_liste_utilisateur)

                    for produit in produits_liste_utilisateur:
                        gestion_stock.retirer_quantite_stock(produit['quantite_depart'], produit['id_produit'])

                    # Construire le message de réponse
                    message = 'La liste utilisateur a bien été créée.'
                    return redirect('logistique_service_medical:liste_utilisateur_creee')  # Retourner une réponse HTTP avec le message et le code 200

            except Exception as e:
                return HttpResponse('Erreur lors de la création de la liste utilisateur.', status=500)

        return HttpResponse('Méthode non autorisée.', status=405)


@user_passes_test(is_admin)
def liste_utilisateur_creee(request):

    return render(request, 'logistique_service_medical/liste_utilisateur_creee.html')


@user_passes_test(is_admin)
def retour(request):
    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    produits_liste_utilisateur = []
    id_liste_utilisateur = 0

    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données soumises par l'utilisateur
        liste_utilisateur_form = ListeUtilisateurForm(request.POST)

        # Vérification si le formulaire est valide
        if liste_utilisateur_form.is_valid():
            # Récupération des données du formulaire
            id_utilisateur = liste_utilisateur_form.cleaned_data['utilisateur']
            gestion_liste_utilisateur.utilisateur.id = int(id_utilisateur)
            gestion_liste_utilisateur.liste_utilisateur.id = gestion_liste_utilisateur.get_id_liste_utilisateur_en_cours()
            produits_liste_utilisateur = gestion_liste_utilisateur.get_1()
            id_liste_utilisateur = gestion_liste_utilisateur.liste_utilisateur.id
    else:
        liste_utilisateur_form = ListeUtilisateurForm()

    context = {'liste_utilisateur_form': liste_utilisateur_form, 'produits_liste_utilisateur': produits_liste_utilisateur, 'id_liste_utilisateur': id_liste_utilisateur}

    return render(request, 'logistique_service_medical/retour.html', context)


@user_passes_test(is_admin)
def verifier_liste_retour(request, id_liste_utilisateur,id_produit):
    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    if request.method == 'POST':
        if id_produit:
            quantite_retour_key = f'quantity_{id_produit}'
            quantite_retour = request.POST.get(quantite_retour_key)
            if quantite_retour is not None:
                try:
                    gestion_liste_utilisateur.liste_utilisateur.id = id_liste_utilisateur
                    gestion_liste_utilisateur.produit.id = id_produit
                    gestion_liste_utilisateur.produit.quantite_retour = int(quantite_retour)

                    gestion_liste_utilisateur.update()

                    response_message = 'Quantité mise à jour avec succès'
                    return HttpResponse(response_message, status=200)


                except Exception as e:
                    return HttpResponse('Erreur lors de la mise à jour de la quantité', status=400)
            else:
                return HttpResponse('Aucune quantité spécifiée dans la requête', status=400)
        else:
            return HttpResponse('Aucun ID d\'association de stock-produit spécifié dans la requête', status=400)
    return HttpResponse('Méthode de requête invalide', status=405)


@user_passes_test(is_admin)
def valider_liste_retour(request, id_liste_utilisateur):

    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    gestion_stock = Gestion_stock()
    produits_retour_verifies = []

    if request.method == 'POST':

        try:
            gestion_liste_utilisateur.liste_utilisateur.id = id_liste_utilisateur
            produits_retour_verifies = gestion_liste_utilisateur.get_1()
            for produit in produits_retour_verifies:
                gestion_stock.ajouter_quantite_stock(produit['quantite_retour'],produit['id_produit'])

            gestion_liste_utilisateur.valider_liste_retour()

            response_message = 'Le stock a été mis à jour'
            return redirect('logistique_service_medical:mise_a_jour_stock')  # Retourner une réponse HTTP avec le message et le code 200


        except Exception as e:

            return HttpResponse("Erreur lors de la validation " + str(e), status=500)

@user_passes_test(is_admin)
def mise_a_jour_stock(request):

    return render(request, 'logistique_service_medical/mise_a_jour_stock.html')


#Partie Utilisateur
@user_passes_test(is_standard_user)
def index_utilisateur(request):
    template = loader.get_template('logistique_service_medical/index_utilisateur.html')
    context = {}
    return HttpResponse(template.render(context, request))



@user_passes_test(is_standard_user)
def ma_liste(request):

    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    produits_liste_utilisateur = []
    id_liste_utilisateur = 0
    utilisateur = request.user
    # Vérifier si l'utilisateur est authentifié
    if utilisateur.is_authenticated:
        # Récupérer l'ID de l'utilisateur
        gestion_liste_utilisateur.utilisateur.id = int(utilisateur.id)
        print(gestion_liste_utilisateur.utilisateur.id)
        gestion_liste_utilisateur.liste_utilisateur.id = gestion_liste_utilisateur.get_id_liste_utilisateur_en_cours()
        produits_liste_utilisateur = gestion_liste_utilisateur.get_1()
        id_liste_utilisateur = gestion_liste_utilisateur.liste_utilisateur.id

        context = {'produits_liste_utilisateur': produits_liste_utilisateur,'id_liste_utilisateur': id_liste_utilisateur}

        return render(request, 'logistique_service_medical/ma_liste.html', context)

    else:
        return redirect('logistique_service_medical:login')



@user_passes_test(is_standard_user)
def remplir_liste_retour(request, id_liste_utilisateur,id_produit):
    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    if request.method == 'POST':
        if id_produit:
            quantite_retour_key = f'quantity_{id_produit}'
            quantite_retour = request.POST.get(quantite_retour_key)
            if quantite_retour is not None:
                try:
                    gestion_liste_utilisateur.liste_utilisateur.id = id_liste_utilisateur
                    gestion_liste_utilisateur.produit.id = id_produit
                    gestion_liste_utilisateur.produit.quantite_retour = int(quantite_retour)

                    gestion_liste_utilisateur.update()

                    response_message = 'Quantité mise à jour avec succès'
                    return HttpResponse(response_message, status=200)


                except Exception as e:
                    return HttpResponse('Erreur lors de la mise à jour de la quantité', status=400)
            else:
                return HttpResponse('Aucune quantité spécifiée dans la requête', status=400)
        else:
            return HttpResponse('Aucun ID d\'association de stock-produit spécifié dans la requête', status=400)
    return HttpResponse('Méthode de requête invalide', status=405)



@user_passes_test(is_admin)
def recherche_archive(request):
    gestion_equipe = Gestion_equipe()
    gestion_deplacement = Gestion_deplacement()
    gestion_liste_depart = Gestion_liste_depart()
    gestion_liste_utilisateur = Gestion_liste_utilisateur()
    listes_archivees = []

    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données soumises par l'utilisateur
        archive_form = ArchiveForm(request.POST)

        # Vérification si le formulaire est valide
        if archive_form.is_valid():
            # Récupération des données du formulaire

            # 1-choisir une équipe pour recuperer un id_equipe
            gestion_equipe.equipe.type_rugby = archive_form.cleaned_data['type_rugby']
            gestion_equipe.equipe.genre = archive_form.cleaned_data['genre']
            gestion_equipe.equipe.categorie_age = archive_form.cleaned_data['categorie_age']

            gestion_liste_depart.equipe.id = gestion_equipe.get_id()
            print(gestion_liste_depart.equipe.id)

            # 2-choisir un deplacement pour recuperer un id_deplacement.

            gestion_deplacement.deplacement.nombre_joueurs = archive_form.cleaned_data['nombre_joueurs']
            gestion_deplacement.deplacement.duree_deplacement = archive_form.cleaned_data['duree_deplacement']
            gestion_deplacement.deplacement.nombre_match = archive_form.cleaned_data['nombre_match']

            gestion_liste_depart.deplacement.id = gestion_deplacement.get_id()
            print(gestion_liste_depart.deplacement.id)

            # 3-obtenir la liste_depart correspondante a l'équipe choisie et au deplacement choisi

            gestion_liste_depart.liste_depart.id = gestion_liste_depart.get_id()

            # 4-obtenir les listes_utilisateurs utilisant la liste depart

            gestion_liste_utilisateur.liste_depart.id = gestion_liste_depart.liste_depart.id
            listes_archivees = gestion_liste_utilisateur.get_id_liste_archivee()
            print(listes_archivees)

            # Convertir les dates en chaînes de caractères dans un format spécifique
            for item in listes_archivees:
                if 'date_liste' in item:
                    item['date_liste'] = item['date_liste'].strftime('%Y-%m-%d')

            # Stocker les données converties dans la session
            request.session['listes_archivees'] = listes_archivees
            # Stocker également les données du formulaire dans la session
            request.session['archive_form_data'] = archive_form.cleaned_data


    else:
        archive_form = ArchiveForm()

    request.session['listes_archivees'] = listes_archivees

    context = {'archive_form': archive_form, 'listes_archivees': listes_archivees}

    return render(request, 'logistique_service_medical/archive.html', context)

def display_archive(request):

    gestion_liste_utilisateur= Gestion_liste_utilisateur()
    archive_form_data = request.session.get('archive_form_data', {})
    archive_form = ArchiveForm(initial=archive_form_data)


    if request.method == 'POST':
        gestion_liste_utilisateur.liste_utilisateur.id = request.POST.get('id_liste_utilisateur')
        print(gestion_liste_utilisateur.liste_utilisateur.id)
        produits_liste_utilisateur = gestion_liste_utilisateur.get_1()
        id_liste_utilisateur = gestion_liste_utilisateur.liste_utilisateur.id
        liste_selectionnee = gestion_liste_utilisateur.get_date_destination()


        listes_archivees = request.session.get('listes_archivees',[])

        context = {'listes_archivees': listes_archivees,'produits_liste_utilisateur': produits_liste_utilisateur,
                   'id_liste_utilisateur': id_liste_utilisateur, 'archive_form': archive_form, 'archive_form_data': archive_form_data, 'liste_selectionnee': liste_selectionnee,}

        return render(request, 'logistique_service_medical/archive.html', context)






