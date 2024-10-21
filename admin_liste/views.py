from django.contrib.auth.decorators import user_passes_test
from registration.permissions import is_admin
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .forms import *
import logging
from admin_stock.business.components.gestion_stock import Gestion_stock
from admin_liste.business.components.gestion_equipe import GestionEquipe
from admin_liste.business.components.gestion_modele_liste import GestionModeleListe
from admin_liste.business.components.gestion_liste_utilisateur import GestionListeUtilisateur
from django.contrib import messages
logger = logging.getLogger("django")


@user_passes_test(is_admin)
def depart_retour(request):

    template = loader.get_template('depart_retour.html')
    context = {}
    return HttpResponse(template.render(context, request))

@user_passes_test(is_admin)
def recherche_modele_liste(request):

    gestion_modele_liste = GestionModeleListe()

    # Recuperer toute les modeles_liste

    modeles_liste = gestion_modele_liste.get_all()
    produits_stock = []
    produits_liste = []
    id_modele_liste = 0
    nom_modele_liste = ""

    if request.method == 'POST':

        # Recuperer les produits du modeles pour les afficher

        gestion_modele_liste.modele_liste.id = request.POST.get('id_modele_liste')
        produits_liste = gestion_modele_liste.get_1()
        id_modele_liste = gestion_modele_liste.modele_liste.id

        nom_modele_liste = request.POST.get('nom_modele_liste')

        produits_stock = gestion_modele_liste.get_liste_vierge()

        for produit_stock in produits_stock:
            for produit_liste in produits_liste:
                if produit_stock['id_produit'] == produit_liste['id_produit']:
                    produit_stock['quantite_depart'] = produit_liste['quantite_depart']
                    produit_stock['quantite_retour'] = produit_liste['quantite_retour']
                    break


    context = {
        'modeles_liste': modeles_liste,
        'produits_stock': produits_stock,
        'produits_liste': produits_liste,
        'id_modele_liste': id_modele_liste,
        'nom_modele_liste': nom_modele_liste,
    }

    return render(request, 'recherche_modele_liste.html', context)


@user_passes_test(is_admin)
def create_modele_liste(request):
    gestion_modele_liste = GestionModeleListe()
    produits_stock = []
    produits_liste = []
    id_modele_liste = 0

    if request.method == 'POST':
        modele_liste_form = ModeleListeForm(request.POST)
        if modele_liste_form.is_valid():
            cleaned_data = modele_liste_form.cleaned_data

            # Vérification des valeurs min/max
            fields_to_check = [
                ('nombre_joueurs_min', 'nombre_joueurs_max'),
                ('duree_deplacement_min', 'duree_deplacement_max'),
                ('nombre_match_min', 'nombre_match_max')
            ]

            has_error = False
            for min_field, max_field in fields_to_check:
                min_value = cleaned_data.get(min_field)
                max_value = cleaned_data.get(max_field)
                if min_value is not None and max_value is not None:
                    if min_value >= max_value:
                        messages.error(request, f"Le champ {min_field} doit être inférieur à {max_field}.")
                        has_error = True

            if not has_error:
                # Procédez à la création du modèle de liste
                gestion_modele_liste.modele_liste.nom_modele_liste = cleaned_data['nom_modele_liste']
                gestion_modele_liste.modele_liste.type_rugby = cleaned_data['type_rugby']
                gestion_modele_liste.modele_liste.nombre_joueurs_min = cleaned_data['nombre_joueurs_min']
                gestion_modele_liste.modele_liste.nombre_joueurs_max = cleaned_data['nombre_joueurs_max']
                gestion_modele_liste.modele_liste.duree_deplacement_min = cleaned_data['duree_deplacement_min']
                gestion_modele_liste.modele_liste.duree_deplacement_max = cleaned_data['duree_deplacement_max']
                gestion_modele_liste.modele_liste.nombre_match_min = cleaned_data['nombre_match_min']
                gestion_modele_liste.modele_liste.nombre_match_max = cleaned_data['nombre_match_max']

                if gestion_modele_liste.get_id() is None:
                    gestion_modele_liste.create()
                    messages.success(request, "Liste créée avec succès.")

                gestion_modele_liste.modele_liste.id = gestion_modele_liste.get_id()
                produits_liste = gestion_modele_liste.get_1()
                id_modele_liste = gestion_modele_liste.modele_liste.id

                produits_stock = gestion_modele_liste.get_liste_vierge()

                for produit_stock in produits_stock:
                    for produit_liste in produits_liste:
                        if produit_stock['id_produit'] == produit_liste['id_produit']:
                            produit_stock['quantite_depart'] = produit_liste['quantite_depart']
                            produit_stock['quantite_retour'] = produit_liste['quantite_retour']
                            break
        else:
            for field, errors in modele_liste_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        modele_liste_form = ModeleListeForm()

    context = {
        'modele_liste_form': modele_liste_form,
        'produits_stock': produits_stock,
        'produits_liste': produits_liste,
        'id_modele_liste': id_modele_liste,
    }

    return render(request, 'create_modele_liste.html', context)


@user_passes_test(is_admin)
def remplir_modele_liste(request, id_modele_liste, id_produit):

    gestion_stock = Gestion_stock()
    gestion_modele_liste = GestionModeleListe()

    # Vérification si le modèle de liste existe
    gestion_modele_liste.modele_liste.id = id_modele_liste
    modele_liste_exist = gestion_modele_liste.test_modele_liste_exist()

    if not modele_liste_exist:
        return JsonResponse({"message": "Le modèle de liste n'a pas encore été validé ou créé."}, status=400)

    if request.method == 'POST':
        if id_produit:
            quantite_depart_key = f'quantity_{id_produit}'
            quantite_depart = request.POST.get(quantite_depart_key)

            if quantite_depart is not None:
                gestion_stock.produit.id = id_produit
                produit = gestion_stock.get_stock_1_produit()

                if int(produit['quantite_stock']) >= int(quantite_depart):
                    try:
                        gestion_modele_liste.produit.id = id_produit
                        gestion_modele_liste.produit.quantite_depart = int(quantite_depart)

                        if gestion_modele_liste.test_association_produit_liste():
                            gestion_modele_liste.delete_association_modele_liste_produit()
                            gestion_modele_liste.update()
                            return HttpResponse('Quantité mise à jour avec succès', status=200)
                        else:
                            gestion_modele_liste.create_association_modele_liste_produit()
                            return HttpResponse('Quantité mise à jour avec succès', status=200)
                    except Exception as e:
                        return JsonResponse({"message": "Erreur lors de la mise à jour de la quantité"}, status=400)
                else:
                    return JsonResponse({"message": "La quantité demandée est supérieure à la quantité en stock"}, status=400)
            else:
                return JsonResponse({"message": "Aucune quantité spécifiée dans la requête"}, status=400)
        else:
            return JsonResponse({"message": "Aucun ID d'association de stock-produit spécifié dans la requête"}, status=400)
    return JsonResponse({"message": "Méthode de requête invalide"}, status=405)



@user_passes_test(is_admin)
def depart(request):
    # Initialisation de vos classes métier
    gestion_equipe = GestionEquipe()
    gestion_modele_liste = GestionModeleListe()
    gestion_liste_utilisateur = GestionListeUtilisateur()
    produits_stock = []
    produits_liste = []
    id_modele_liste = 0
    id_liste_utilisateur = 0

    # Récupération de toutes les équipes
    equipes = gestion_equipe.get_all()

    if request.method == 'POST':
        equipe_utilisateur_form = EquipeUtilisateurForm(request.POST)
        if equipe_utilisateur_form.is_valid():
            gestion_equipe.equipe.type_rugby = equipe_utilisateur_form.cleaned_data['type_rugby']
            gestion_equipe.equipe.genre = equipe_utilisateur_form.cleaned_data['genre']
            gestion_equipe.equipe.categorie_age = equipe_utilisateur_form.cleaned_data['categorie_age']

            gestion_liste_utilisateur.liste_utilisateur.equipe.id = gestion_equipe.get_id()
            gestion_liste_utilisateur.liste_utilisateur.nombre_joueurs = equipe_utilisateur_form.cleaned_data['nombre_joueurs']
            gestion_liste_utilisateur.liste_utilisateur.duree_deplacement = equipe_utilisateur_form.cleaned_data['duree_deplacement']
            gestion_liste_utilisateur.liste_utilisateur.nombre_match = equipe_utilisateur_form.cleaned_data['nombre_match']
            gestion_liste_utilisateur.liste_utilisateur.utilisateur.id = int(equipe_utilisateur_form.cleaned_data['utilisateur'])
            gestion_liste_utilisateur.liste_utilisateur.date = equipe_utilisateur_form.cleaned_data['date_depart']
            gestion_liste_utilisateur.liste_utilisateur.destination = equipe_utilisateur_form.cleaned_data['destination']

            type_rugby = int(gestion_equipe.equipe.type_rugby)
            nombre_joueurs = gestion_liste_utilisateur.liste_utilisateur.nombre_joueurs
            duree_deplacement = gestion_liste_utilisateur.liste_utilisateur.duree_deplacement
            nombre_match = gestion_liste_utilisateur.liste_utilisateur.nombre_match

            if gestion_liste_utilisateur.test_liste_en_cours():
                messages.error(request, "Une liste est déjà en cours pour cet utilisateur")
                return redirect('admin_liste:depart')

            modeles_liste = gestion_modele_liste.get_all()
            modele_trouve = False
            for modele in modeles_liste:
                if (modele['type_rugby'] == type_rugby and
                    modele['nombre_joueurs_min'] <= nombre_joueurs <= modele['nombre_joueurs_max'] and
                    modele['duree_deplacement_min'] <= duree_deplacement <= modele['duree_deplacement_max'] and
                    modele['nombre_match_min'] <= nombre_match <= modele['nombre_match_max']):
                    id_modele_liste = modele['id_modele_liste']
                    modele_trouve = True
                    break

            if not modele_trouve:
                messages.error(request, "Aucun modèle de liste ne correspond aux critères.")
                return redirect('admin_liste:depart')

            gestion_liste_utilisateur.liste_utilisateur.modele_liste.id = id_modele_liste
            gestion_liste_utilisateur.create()
            gestion_liste_utilisateur.liste_utilisateur.id = gestion_liste_utilisateur.get_id()
            id_liste_utilisateur = gestion_liste_utilisateur.liste_utilisateur.id
            gestion_liste_utilisateur.create_association_liste_utilisateur_produit()

            produits_liste = gestion_liste_utilisateur.get_1()
            produits_stock = gestion_modele_liste.get_liste_vierge()

            for produit_stock in produits_stock:
                for produit_liste in produits_liste:
                    if produit_stock['id_produit'] == produit_liste['id_produit']:
                        produit_stock['quantite_depart'] = produit_liste['quantite_depart']
                        produit_stock['quantite_retour'] = produit_liste['quantite_retour']
                        break

            messages.success(request, "La liste a été créée avec succès.")
        else:
            messages.error(request, "Le formulaire n'est pas valide. Veuillez vérifier les informations saisies.")

    else:
        equipe_utilisateur_form = EquipeUtilisateurForm()

    context = {
        'equipes': equipes,
        'equipe_utilisateur_form': equipe_utilisateur_form,
        'produits_stock': produits_stock,
        'produits_liste': produits_liste,
        'id_liste_utilisateur': id_liste_utilisateur,
    }

    return render(request, 'depart.html', context)

@user_passes_test(is_admin)
def remplir_liste_utilisateur(request, id_liste_utilisateur, id_produit):

    gestion_stock = Gestion_stock()
    gestion_modele_liste = GestionModeleListe()
    gestion_liste_utilisateur = GestionListeUtilisateur()
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
                        gestion_liste_utilisateur.liste_utilisateur.id = id_liste_utilisateur
                        gestion_liste_utilisateur.produit.id = id_produit
                        gestion_liste_utilisateur.produit.quantite_depart = int(quantite_depart)


                        if gestion_liste_utilisateur.test_association_produit_liste():

                            gestion_liste_utilisateur.delete_association_liste_utilisateur_produit()
                            gestion_liste_utilisateur.update_depart()
                            response_message = 'Quantité mise à jour avec succès'
                            return HttpResponse(response_message, status=200)

                        else:
                            gestion_liste_utilisateur.create_association_liste_utilisateur_produit()  # Utilise la méthode update_quantity de Gestion_stock
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
def create_liste_utilisateur(request, id_liste_utilisateur):

    gestion_stock = Gestion_stock()
    gestion_liste_utilisateur = GestionListeUtilisateur()

    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données soumises par l'utilisateur

        gestion_liste_utilisateur.liste_utilisateur.id = id_liste_utilisateur
        gestion_liste_utilisateur.get_1()

        produits_liste_utilisateur = gestion_liste_utilisateur.get_1()
        print(produits_liste_utilisateur)

        for produit in produits_liste_utilisateur:
            gestion_stock.retirer_quantite_stock(produit['quantite_depart'], produit['id_produit'])

                    # Construire le message de réponse


        return JsonResponse({"message":'Le stock a ete mis à jour avec succes.'}, status=200)

        # Si la méthode n'est pas POST, renvoyer une redirection vers l'index
    return redirect('depart')


@user_passes_test(is_admin)
def liste_utilisateur_creee(request):

    return render(request, 'liste_utilisateur_creee.html')


@user_passes_test(is_admin)
def retour(request):
    gestion_liste_utilisateur = GestionListeUtilisateur()
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
    gestion_liste_utilisateur = GestionListeUtilisateur()
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

    gestion_liste_utilisateur = GestionListeUtilisateur()
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
    gestion_equipe = GestionEquipe()
    gestion_modele_liste = GestionModeleListe()
    gestion_liste_utilisateur = GestionListeUtilisateur()
    listes_archivees = []

    if request.method == 'POST':
        archive_form = ArchiveForm(request.POST)
        if archive_form.is_valid():
            cleaned_data = archive_form.cleaned_data

            gestion_modele_liste.modele_liste.type_rugby = cleaned_data['type_rugby']

            nombre_joueurs_min, nombre_joueurs_max = map(int, cleaned_data['nombre_joueurs'].split('-'))
            gestion_modele_liste.modele_liste.nombre_joueurs_min = nombre_joueurs_min
            gestion_modele_liste.modele_liste.nombre_joueurs_max = nombre_joueurs_max

            duree_deplacement_min, duree_deplacement_max = map(int, cleaned_data['duree_deplacement'].split('-'))
            gestion_modele_liste.modele_liste.duree_deplacement_min = duree_deplacement_min
            gestion_modele_liste.modele_liste.duree_deplacement_max = duree_deplacement_max

            nombre_match_min, nombre_match_max = map(int, cleaned_data['nombre_match'].split('-'))
            gestion_modele_liste.modele_liste.nombre_match_min = nombre_match_min
            gestion_modele_liste.modele_liste.nombre_match_max = nombre_match_max

            gestion_modele_liste.modele_liste.id = gestion_modele_liste.get_id_multiples_parametres()

            gestion_liste_utilisateur.liste_utilisateur.modele_liste.id = gestion_modele_liste.modele_liste.id
            print(gestion_liste_utilisateur.liste_utilisateur.modele_liste.id)
            listes_archivees = gestion_liste_utilisateur.get_listes_archivees()


            for item in listes_archivees:
                if 'date_liste' in item:
                    item['date_liste'] = item['date_liste'].strftime('%Y-%m-%d')

            request.session['listes_archivees'] = listes_archivees
            request.session['archive_form_data'] = cleaned_data
    else:
        archive_form = ArchiveForm()

    request.session['listes_archivees'] = listes_archivees

    context = {'archive_form': archive_form, 'listes_archivees': listes_archivees}

    return render(request, 'archive.html', context)
@user_passes_test(is_admin)
def display_archive(request):

    gestion_liste_utilisateur= GestionListeUtilisateur()
    archive_form_data = request.session.get('archive_form_data', {})
    archive_form = ArchiveForm(initial=archive_form_data)


    if request.method == 'POST':
        gestion_liste_utilisateur.liste_utilisateur.id = request.POST.get('id_liste_utilisateur')
        print(gestion_liste_utilisateur.liste_utilisateur.id)
        produits_liste_utilisateur = gestion_liste_utilisateur.get_1()
        id_liste_utilisateur = gestion_liste_utilisateur.liste_utilisateur.id
        liste_selectionnee = gestion_liste_utilisateur.get_date_destination()
        print(liste_selectionnee)


        listes_archivees = request.session.get('listes_archivees',[])

        context = {'listes_archivees': listes_archivees,'produits_liste_utilisateur': produits_liste_utilisateur,
                   'id_liste_utilisateur': id_liste_utilisateur, 'archive_form': archive_form, 'archive_form_data': archive_form_data, 'liste_selectionnee': liste_selectionnee,}

        return render(request, 'archive.html', context)






