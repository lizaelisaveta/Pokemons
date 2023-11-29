from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterView, register_confirm

urlpatterns = [
    path('', views.list_names, name='list_names'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_results, name='search_results'),
    path('detail/<int:id>/', views.details, name='details'),
    path('fights/<int:id>/', views.fights, name='fights'),
    path('fight/<int:id>/<int:enemy_id>', views.fights1, name='fights1'),
    path('fastfight/<int:id>/', views.fastfights, name='fastfights'),
    path('sendresult/', views.send_result, name='send_result'),
    path('savedoc/<int:id>/', views.save_doc_about, name='save_doc_about'),
    path('downloadpokemons/', views.download_pokemons, name='download_pokemons'),
    path('register/', RegisterView.as_view(), name="register"),
    path("register_confirm/<token>/", register_confirm, name="register_confirm"),
]
