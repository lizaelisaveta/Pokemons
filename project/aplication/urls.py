from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_names, name='list_names'),
    path('search/', views.search_results, name='search_results'),
    path('detail/<str:name>/', views.details, name='details'),
    path('fight/<str:name>/', views.fights, name='fights'),
    path('fastfight/', views.fights_fast, name='fights_fast'),
    path('simplefight/', views.fights_simple, name='fights_simple'),
]
