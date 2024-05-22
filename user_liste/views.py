from django.contrib.auth.decorators import user_passes_test
from registration.permissions import is_admin, is_standard_user
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
import logging
from admin_liste.business.components.gestion_liste_utilisateur import Gestion_liste_utilisateur
logger = logging.getLogger("django")

#Partie Utilisateur
@user_passes_test(is_standard_user)
def index_utilisateur(request):
    template = loader.get_template('index_utilisateur.html')
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

        return render(request, 'ma_liste.html', context)

    else:
        return redirect('registration:login')

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

                    message = 'Quantité mise à jour avec succès'
                    return JsonResponse({"message": message}, status=200)


                except Exception as e:
                    return JsonResponse({"message":'Erreur lors de la mise à jour de la quantité'}, status=400)
            else:
                return JsonResponse({"message":'Aucune quantité spécifiée dans la requête'}, status=400)
        else:
            return JsonResponse({"message":'Aucun ID d\'association de stock-produit spécifié dans la requête'}, status=400)
    return JsonResponse({"message":'Méthode de requête invalide'}, status=405)

