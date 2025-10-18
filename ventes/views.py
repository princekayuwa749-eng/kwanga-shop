from django.shortcuts import render, get_object_or_404, redirect
from .models import Produit, Commande, LigneCommande
from .forms import AjouterAuPanierForm, CheckoutForm
from django.contrib import messages
from django.db import transaction
from decimal import Decimal


# --- Liste des produits ---
def liste_produits(request):
    produits = Produit.objects.filter(est_actif=True)
    return render(request, 'ventes/product_list.html', {'products': produits})


# --- Détail d'un produit ---
def detail_produit(request, slug):
    produit = get_object_or_404(Produit, slug=slug, est_actif=True)
    form = AjouterAuPanierForm()
    return render(request, 'ventes/product_detail.html', {'product': produit, 'form': form})


# --- Gestion interne du panier en session ---
def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


# --- Ajouter un produit au panier ---
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id, est_actif=True)
    if request.method == 'POST':
        form = AjouterAuPanierForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantite']
            cart = _get_cart(request)
            pid = str(produit_id)
            cart[pid] = cart.get(pid, 0) + qty

            # Vérification stock
            if cart[pid] > produit.stock:
                messages.error(request, f"Stock insuffisant. Stock actuel: {produit.stock}")
                return redirect(produit.get_absolute_url())

            _save_cart(request, cart)
            messages.success(request, f"{produit.nom} ajouté au panier.")
            return redirect('cart')
    return redirect('detail_produit', slug=produit.slug)


# --- Retirer un produit du panier ---
def retirer_du_panier(request, produit_id):
    cart = _get_cart(request)
    pid = str(produit_id)
    if pid in cart:
        del cart[pid]
        _save_cart(request, cart)
        messages.success(request, 'Article supprimé du panier.')
    return redirect('cart')


# --- Afficher le panier ---
def panier(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0.00')
    for pid, qty in cart.items():
        produit = get_object_or_404(Produit, id=int(pid))
        item_total = produit.prix * qty
        total += item_total
        items.append({
            'produit': produit,
            'quantite': qty,
            'prix_total': item_total,
        })
    return render(request, 'ventes/cart.html', {'items': items, 'total': total})


# --- Checkout / passer la commande ---
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Votre panier est vide.")
        return redirect('liste_produits')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Création de la commande
                commande = Commande.objects.create(
                    nom_client=form.cleaned_data['nom_client'],
                    email=form.cleaned_data['email'],
                    adresse=form.cleaned_data['adresse'],
                    statut='pending'
                )
                # Création des lignes de commande et mise à jour stock
                for pid, qty in cart.items():
                    produit = get_object_or_404(Produit, id=int(pid))
                    LigneCommande.objects.create(
                        commande=commande,
                        produit=produit,
                        prix=produit.prix,
                        quantite=qty
                    )
                    produit.stock -= qty
                    produit.save()
                
                # Vider le panier après validation
                request.session['cart'] = {}
            
            messages.success(request, f"Commande #{commande.id} passée avec succès !")
            return redirect('success')
    else:
        form = CheckoutForm()

    return render(request, 'ventes/checkout.html', {'form': form, 'cart': cart})


# --- Page de succès après commande ---
def success(request):
    return render(request, 'ventes/success.html')