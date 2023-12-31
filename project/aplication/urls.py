from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_names, name='list_names'),
    path('search/', views.search_results, name='search_results'),
    path('detail/<int:id>/', views.details, name='details'),
    path('fights/<int:id>/', views.fights, name='fights'),
    path('fight/<int:id>/<int:enemy_id>', views.fights1, name='fights1'),
    path('fastfight/<int:id>/', views.fastfights, name='fastfights'),
    path('sendresult/', views.send_result, name='send_result'),
]
