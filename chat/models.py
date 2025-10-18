from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    expediteur = models.ForeignKey(User, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(User, related_name='messages_recus', on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expediteur} → {self.destinataire}: {self.contenu[:30]}"