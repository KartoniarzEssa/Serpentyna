from django.shortcuts import render, redirect
from django.contrib.auth.signals import *
from django.dispatch import receiver
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from player_queue.models import url
from .models import ActiveUsers
import yt_dlp


# Create your views here.

def auth(request):
    if len(ActiveUsers.objects.all()) >= 1:
        return render(request, 'session_busy.html')
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('/player/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/player/')
        else:
            return render(request, 'login.html', {'error': 'Niepoprawne dane logowania!'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/player/login')

@login_required
def player(request):
    if len(ActiveUsers.objects.all()) >= 1 and not(request.user.username != ActiveUsers.objects.first()):
        return render(request, 'session_busy.html')
    info = get_latest_url()
    context = {
            'url': info['url'],
            'title': info['title'],
            'thumbnail': info['thumbnail']
            }
    return render(request, 'player.html', context)

@login_required
def next_media(request):
    if len(ActiveUsers.objects.all()) >= 1 and not(request.user.username != ActiveUsers.objects.first()):
        JsonResponse({'url': 'Sesja zajęta!'})
    if request.method == 'GET':
        return JsonResponse(get_latest_url())
    
# Not views
def get_latest_url():
    yt_url = str(url.objects.all().first())
    if yt_url != 'None':
        ydl_opts = {
            'format': 'bestaudio/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ytdlp:
            info = ytdlp.extract_info(yt_url, download=False)
        yt_url_pk = url.objects.all().first().pk
        url.objects.get(pk=yt_url_pk).delete()
        return {
            'url': info['url'],
            'title': info['title'],
            'thumbnail': info['thumbnail']
            }
    return {
            'url': '',
            'title': 'Kolejka aktualnie pusta',
            'thumbnail': ''
            }
    
@receiver(user_logged_out)
def remove_active_user(request, **kwargs):
    if not('admin' in request.META['PATH_INFO']):
        is_logged = ActiveUsers.objects.all()
        is_logged.delete()
    
@receiver(user_logged_in)
def add_active_user(request, **kwargs):
    if request.method == 'POST' and not('admin' in request.META['PATH_INFO']):
        username = request.POST['username']
        is_logged = ActiveUsers(active_users=username)
        is_logged.save()
        