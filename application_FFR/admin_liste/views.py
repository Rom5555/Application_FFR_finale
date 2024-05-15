from django.contrib.auth.decorators import user_passes_test
from registration.permissions import is_admin, is_standard_user
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .forms import *
import logging
from admin_stock.business.components.gestion_stock import Gestion_stock
from admin_liste.business.components.gestion_equipe import Gestion_equipe
from admin_liste.business.components.gestion_deplacement import Gestion_deplacement
from admin_liste.business.components.gestion_liste_depart import Gestion_liste_depart
from admin_liste.business.components.gestion_liste_utilisateur import Gestion_liste_utilisateur
logger = logging.getLogger("django")

#Gestion Liste

@user_passes_test(is_admin)
def depart_retour(request):

    template = loader.get_template('depart_retour.html')
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
    id_liste_depart = 0

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
    return render(request, 'depart.html', context)

@user_passes_test(is_admin)
def remplir_liste_depart(request, id_liste_depart, id_produit):

    gestion_stock = Gestion_stock()
    gestion_liste_depart = Gestion_liste_depart()
    if request.method == 'POST':

        if id_produit:
            quantite_depart_key = f'quantity_{id_produit}'
            quantite_depart = request.POST.get(quantite_depart_key)

            if quantite_depart is not None:


                gestion_stock.produit.id = id_produit
                produit = gestion_stock.get_stock_1_produit()
                print(produit)

                if int(produit['quantite_stock']) >= int(quantite_depart):
                    try:
                        gestion_liste_depart.liste_depart.id = id_liste_depart
                        gestion_liste_depart.produit.id = id_produit
                        gestion_liste_depart.produit.quantite_depart = int(quantite_depart)


                        if gestion_liste_depart.test_association_produit_liste():

                            gestion_liste_depart.delete_association_liste_depart_produit()
                            gestion_liste_depart.update()
                            response_message = 'Quantité mise à jour avec succès'
                            return HttpResponse(response_message, status=200)

                        else:
                            gestion_liste_depart.create_association_liste_depart_produit()  # Utilise la méthode update_quantity de Gestion_stock
                            response_message = 'Quantité mise à jour avec succès'
                            return HttpResponse(response_message, status=200)



                    except Exception as e:
                        return JsonResponse({"message":'Erreur lors de la mise à jour de la quantité'}, status=400)

                else:
                    return JsonResponse({"message":'La quantite_depart est superieur à la quantite_stock'}, status=400)

            else:
                return JsonResponse({"message":'Aucune quantité spécifiée dans la requête'}, status=400)
        else:
            return JsonResponse({"message":'Aucun ID d\'association de stock-produit spécifié dans la requête'}, status=400)
    return JsonResponse({"message":'Méthode de requête invalide'}, status=405)

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
                    message = "Une liste est déjà en cours pour cet utilisateur"
                    return JsonResponse({"message": message}, status=405)


                elif not gestion_liste_utilisateur.create():
                    print("La liste utilisateur existe déjà")
                    message = "La liste utilisateur existe déjà"
                    return JsonResponse({"message": message}, status=400)

                else:

                    gestion_liste_utilisateur.create()
                    gestion_liste_utilisateur.liste_utilisateur.id = gestion_liste_utilisateur.get_id()
                    # Remplissage de la liste utilisateur
                    gestion_liste_utilisateur.create_association_liste_utilisateur_produit()
                    gestion_liste_utilisateur.get_1()

                    produits_liste_utilisateur=gestion_liste_utilisateur.get_1()

                    for produit in produits_liste_utilisateur:
                        gestion_stock.retirer_quantite_stock(produit['quantite_depart'], produit['id_produit'])

                    # Construire le message de réponse
                    message = 'La liste utilisateur a bien été créée.'
                    return JsonResponse({"message": message}, status=200)

            except Exception as e:
                return JsonResponse({"message": "Erreur lors de la création de la liste utilisateur."}, status=500)

        return JsonResponse({"message": "Méthode non autorisée."}, status=405)

    return JsonResponse({"message": "Méthode non autorisée."}, status=405)

@user_passes_test(is_admin)
def liste_utilisateur_creee(request):

    return render(request, 'liste_utilisateur_creee.html')


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

    return render(request, 'retour.html', context)


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

                    message = 'Quantité mise à jour avec succès'
                    return JsonResponse({"message": message}, status=200)


                except Exception as e:
                    return JsonResponse({"message":"Erreur lors de la mise à jour de la quantité"} , status=400)
            else:
                return JsonResponse({"message": "Aucune quantité spécifiée dans la requête"}, status=400)
        else:
            return JsonResponse({"message": 'Aucun ID d\'association de stock-produit spécifié dans la requête'}, status=400)
    return JsonResponse({"message": 'Méthode de requête invalide'}, status=405)


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

            message = 'Le stock a été mis à jour'
            return JsonResponse({"message": message}, status = 200) # Retourner une réponse HTTP avec le message et le code 200


        except Exception as e:

            return JsonResponse({"message": "Erreur lors de la validation" + str(e)}, status=500)

@user_passes_test(is_admin)
def mise_a_jour_stock(request):

    return render(request, 'mise_a_jour_stock.html')



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

    return render(request, 'archive.html', context)

@user_passes_test(is_admin)
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

        return render(request, 'archive.html', context)






