from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('produit/<slug:slug>/', views.detail_produit, name='detail_produit'),
    path('panier/', views.panier, name='cart'),
    path('panier/ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/retirer/<int:produit_id>/', views.retirer_du_panier, name='retirer_du_panier'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
]