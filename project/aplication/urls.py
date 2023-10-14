from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_names, name='list_names'),
    path('search/', views.search_results, name='search_results'),
    path('detail/<str:name>/', views.details, name='details'),
    path('fights/<str:name>/', views.fights, name='fights'),
    path('fight/<str:name>/<str:enemy_name>', views.fights1, name='fights1'),
    path('fastfight/<str:name>/', views.fastfights, name='fastfights'),
    path('sendresult/', views.send_result, name='send_result'),
]
