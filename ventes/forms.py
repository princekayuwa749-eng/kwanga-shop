from django import forms


class AjouterAuPanierForm(forms.Form):
    quantite = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Quantité"
    )


class CheckoutForm(forms.Form):
    nom_client = forms.CharField(
        max_length=200,
        label="Nom complet"
    )
    email = forms.EmailField(
        label="Adresse e-mail"
    )
    adresse = forms.CharField(
        widget=forms.Textarea,
        label="Adresse de livraison"
    )