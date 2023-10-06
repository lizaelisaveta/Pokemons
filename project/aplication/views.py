from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Pokemon
import requests

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
    
    count_pages = 20
    paginator = Paginator(names, count_pages)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'aplication/list_names.html', {'names': page_obj.object_list, 'counts': counts, 'paginator': paginator, 'page_obj': page_obj, 'query': query})

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
    matching_names = [name for name in names if name.lower().startswith(query.lower())]
    
    count_pages = 20
    paginator = Paginator(matching_names, count_pages)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'aplication/list_names.html', {'names': page_obj.object_list, 'counts': len(matching_names), 'paginator':paginator, 'page_obj': page_obj, 'query': query})
