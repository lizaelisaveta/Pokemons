from django.shortcuts import render
from .models import Pokemon
import requests

def list_names(request):
    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
    name_poke_json = name_poke.json()
    names = [result['name'] for result in name_poke_json['results']]

    return render(request, 'aplication/list_names.html', {'names': names, 'counts': counts})


def search_results(request):
    query = request.GET.get('query')
    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
    name_poke_json = name_poke.json()
    names = [result['name'] for result in name_poke_json['results']]
    matching_names = [name for name in names if name.lower().startswith(query.lower())]
    
    return render(request, 'aplication/list_names.html', {'names': matching_names, 'counts': len(matching_names)})
