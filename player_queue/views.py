from django.shortcuts import render
from .forms import *

# Create your views here.

def player_queue(request):
    
    yt_url_form = url_form()
    if request.method == 'POST':
        yt_url_form = url_form(request.POST)
        
    context = {'yt_url':yt_url_form}
    
    if yt_url_form.is_valid():
        yt_url_form.save(commit=False)
        yt_url_form.data = ({})
    
    return render(request, 'add_queue.html', context)