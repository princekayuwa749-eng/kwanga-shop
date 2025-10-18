from django.db import models
from django.urls import reverse


class Produit(models.Model):
    nom = models.CharField("Nom du produit", max_length=200)
    slug = models.SlugField("Identifiant URL", max_length=200, unique=True)
    description = models.TextField("Description", blank=True)
    prix = models.DecimalField("Prix (CDF)", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Quantité en stock", default=0)
    image = models.ImageField("Image", upload_to='produits/', null=True, blank=True)
    est_actif = models.BooleanField("Disponible", default=True)
    cree_le = models.DateTimeField("Date d'ajout", auto_now_add=True)

    class Meta:
        ordering = ['-cree_le']
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.nom

    # Correction du nom pour correspondre au urls.py
    def get_absolute_url(self):
        return reverse('detail_produit', args=[self.slug])


class Commande(models.Model):
    STATUT_CHOIX = [
        ('pending', 'En attente'),
        ('paid', 'Payée'),
        ('shipped', 'Expédiée'),
        ('cancelled', 'Annulée'),
    ]

    nom_client = models.CharField("Nom du client", max_length=200)
    email = models.EmailField("Email")
    adresse = models.TextField("Adresse de livraison")
    cree_le = models.DateTimeField("Date de commande", auto_now_add=True)
    statut = models.CharField("Statut", max_length=20, choices=STATUT_CHOIX, default='pending')

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"Commande #{self.id} - {self.nom_client}"

    def prix_total(self):
        return sum(item.prix_total() for item in self.items.all())


class LigneCommande(models.Model):
    commande = models.ForeignKey(Commande, related_name='items', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, verbose_name="Produit", on_delete=models.PROTECT)
    prix = models.DecimalField("Prix unitaire (CDF)", max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField("Quantité")

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    def prix_total(self):
        return self.prix * self.quantite