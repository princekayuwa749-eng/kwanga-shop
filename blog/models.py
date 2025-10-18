from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    STATUT = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    contenu = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    statut = models.CharField(max_length=10, choices=STATUT, default='draft')
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)
    publie_le = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-publie_le', '-cree_le']

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])