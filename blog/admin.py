from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titre', 'slug', 'auteur', 'statut', 'publie_le')
    list_filter = ('statut', 'publie_le', 'auteur')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'publie_le'
    ordering = ('-publie_le',)