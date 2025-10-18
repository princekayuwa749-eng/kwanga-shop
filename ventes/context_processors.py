def cart_item_count(request):
    """
    Retourne le nombre total d'articles dans le panier pour l'afficher dans le template.
    """
    cart = request.session.get('cart', {})
    total = sum(cart.values()) if isinstance(cart, dict) else 0
    return {'cart_item_count': total}