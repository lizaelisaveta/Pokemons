from email.mime import image
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pokemon
import requests

BASE_URL = 'https://pokeapi.co/api/v2/pokemon'

class Pokemon:
 
    def __init__(self, name, image, url):
        self.url = url
        self.id = url.split('/')[-2]
        self.name = name   
        self.image = image

    def get_details(self, id):
        response = requests.get(f"{BASE_URL}/{id}").json()
        hp = response['stats'][0]['base_stat']
        attack = response['stats'][1]['base_stat']
        speed = response['stats'][-1]['base_stat']
        arrays = [hp, attack, speed]
        return arrays


def list_names(request):
    query = ''
    if 'search_query' in request.session:
        query = request.session['search_query']
        
    if request.GET.get('query'):
        query = request.GET.get('query')
        request.session['search_query'] = query


    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
    name_poke_json = name_poke.json()
    names = [result['name'] for result in name_poke_json['results']]
    urls = [result['url'] for result in name_poke_json['results']]
    images = display_images(name_poke_json, counts)
    
    pokemon_data = [[name for name in names], [image for image in images], [url for url in urls]]
    pokemon_list = [Pokemon(name, image, url) for name, image, url in zip(*pokemon_data)]
    
    
    count_pages = 20
    paginator = Paginator(pokemon_list, count_pages)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list, 'counts': counts, 'paginator': paginator, 'page_obj': page_obj, 'query': query})

def search_results(request):
    query = ''
    if 'search_query' in request.session:
        query = request.session['search_query']
        
    if request.GET.get('query'):
        query = request.GET.get('query')
        request.session['search_query'] = query

        
    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
    name_poke_json = name_poke.json()
    names = [result['name'] for result in name_poke_json['results']]
    urls = [result['url'] for result in name_poke_json['results']]
    matching_names = [name for name in names if name.lower().startswith(query.lower())]
    
    images = display_images(name_poke_json, counts)
    
    pokemon_data = [[name for name in matching_names], [image for image in images], [url for url in urls]]
    pokemon_list = [Pokemon(name, image, url) for name, image, url in zip(*pokemon_data)]
    
    count_pages = 20
    paginator = Paginator(pokemon_list, count_pages)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list, 'counts': len(matching_names), 'paginator':paginator, 'page_obj': page_obj, 'query': query})


def display_images(name_poke_json, counts):
    pokemons = name_poke_json['results']
    
    pokeImages = []
    for pokemon in pokemons:
        pokeID = pokemon['url'].split('/')[-2]
        pokeImage = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokeID}.png"
        pokeImages.append(pokeImage)

    return  pokeImages



def details(request, name):
    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
    name_poke_json = name_poke.json()
    names = [result['name'] for result in name_poke_json['results']]
    urls = [result['url'] for result in name_poke_json['results']]
    matching_names = [name for name in names if name.lower().startswith(name.lower())]
    
    images = display_images(name_poke_json, counts)
    
    pokemon_data = [[name for name in matching_names], [image for image in images], [url for url in urls]]
    pokemon_list = [Pokemon(nam, image, url) for nam, image, url in zip(*pokemon_data) if nam == name]

    details_about = pokemon_list[0].get_details(pokemon_list[0].id)
    
    
    return render(request, 'aplication/details.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2]})


def fights(request):
    teses = 1
    return render(request, 'aplication/details.html', {'teses': teses})