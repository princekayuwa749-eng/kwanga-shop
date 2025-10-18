from django.contrib import admin
from .models import Produit, Commande, LigneCommande


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'est_actif')
    prepopulated_fields = {'slug': ('nom',)}
    search_fields = ('nom', 'description')


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    readonly_fields = ('prix',)
    extra = 0


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom_client', 'email', 'cree_le', 'statut')
    inlines = [LigneCommandeInline]
    list_filter = ('statut', 'cree_le')