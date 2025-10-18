from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.utils import timezone

def post_list(request):
    # Récupère uniquement les posts publiés
    posts = Post.objects.filter(statut='published', publie_le__lte=timezone.now())
    paginator = Paginator(posts, 6)  # 6 articles par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, slug):
    # Cherche le post par slug et statut
    post = get_object_or_404(Post, slug=slug, statut='published', publie_le__lte=timezone.now())
    return render(request, 'blog/post_detail.html', {'post': post})