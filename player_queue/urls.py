from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_queue, name='queue'),
]
