from django.contrib.auth.decorators import user_passes_test
from registration.permissions import is_admin, is_standard_user
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
import logging
from admin_stock.business.components.gestion_stock import Gestion_stock
logger = logging.getLogger("django")

# Gestion stock

@user_passes_test(is_admin)
def stock_consommables(request):
    gestion_stock = Gestion_stock()
    consommables = gestion_stock.get_1()
    context = {'consommables': consommables}
    return render(request, 'stock_consommables.html', context)

@user_passes_test(is_admin)
def select_stock(request):
    gestion_stock = Gestion_stock()
    liste_stocks = gestion_stock.get_all()  # Utilise la méthode get_all de Gestion_stock
    context = {
        'liste_stocks': liste_stocks,
    }
    return render(request, 'select_stock.html', context)


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
    return render(request, 'display_produits.html', context)


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

    return render(request, 'produit_list.html',
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
                return redirect('admin_stock:produit_list')

            except Exception as e:
                print(e)
                save_error = True

    # Si l'ajout du produit a échoué, ne pas stocker de message de succès dans la session
    if save_error:
        messages.error(request, 'Erreur lors de l\'ajout du produit.')

    return render(request, 'produit_list.html',
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
    return redirect('admin_stock:produit_list')
