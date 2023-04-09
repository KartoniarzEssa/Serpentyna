from django.urls import path
from . import views

urlpatterns = [
    path('', views.player, name='player'),
    path('next_media/', views.next_media, name='next-media'),
    path('login/', views.auth, name='login'),
    path('logout/', views.logout_view, name='logout'),
]