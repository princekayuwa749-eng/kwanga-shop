from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Message

# Page principale du chat
def chat_view(request):
    from .forms import MessageForm  # si tu as un formulaire
    form = MessageForm()
    messages = Message.objects.all().order_by('date_envoi')
    return render(request, 'chat/chat.html', {'form': form, 'messages': messages})

# Envoyer un message
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        contenu = request.POST.get('contenu', '').strip()
        if contenu:
            msg = Message.objects.create(
                expediteur=request.user,
                contenu=contenu,
                date_envoi=timezone.now()
            )
            return JsonResponse({'status': 'ok', 'message_id': msg.id})
    return JsonResponse({'status': 'error'})

# Récupérer les messages
def get_messages(request):
    messages = Message.objects.all().order_by('date_envoi')
    data = []
    for m in messages:
        data.append({
            'expediteur': m.expediteur.username,
            'contenu': m.contenu,
            'date_envoi': m.date_envoi.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse(data, safe=False)