from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_names, name='list_names'),
    path('search/', views.search_results, name='search_results'),
    path('detail/<str:name>/', views.details, name='details'),
    path('fight/', views.fights, name='fights'),
]
