from email.mime import image
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Fight
import requests
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText


BASE_URL = 'https://pokeapi.co/api/v2/pokemon'

class Pokemon:
 
    def __init__(self, name, image,url,id=None):
        self.url = url
        self.name = name   
        self.image = image
        if id:
            self.id = id
        else:
            self.id = url.split('/')[-2]


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

def display_images(name_poke_json, indexes):
    pokemons = name_poke_json['results']

    pokeImages = []
    for pokemon in pokemons:
        pokeID = pokemon['url'].split('/')[-2]
        pokeImage = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokeID}.png"
        pokeImages.append(pokeImage)

    return  pokeImages


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

    indexes = [index for index, name in enumerate(names) if name in matching_names]
    indexes = [index+1 for index in indexes]
    
    images = display_images_serach(indexes)
    
    pokemon_data = [[name for name in matching_names], [image for image in images],[url for url in urls], [ind for ind in indexes] ]
    pokemon_list = [Pokemon(name, image,url,id) for name, image, url,id in zip(*pokemon_data)]
    
    count_pages = 20
    paginator = Paginator(pokemon_list, count_pages)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list, 'ids': indexes,'counts': len(matching_names), 'paginator':paginator, 'page_obj': page_obj, 'query': query})


def display_images_serach(indexes):
    if indexes:
        pokeImages = []
        for i in indexes:
            pokeID = i
            pokeImage = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokeID}.png"
            pokeImages.append(pokeImage)
        return  pokeImages
    pokeImage = "https://img.icons8.com/color/96/pokeball--v1.png"
    return  pokeImage



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


def fights(request, name):
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

    random_index = [random.randint(1, counts-1)]
    enemy_images = display_images_serach(random_index)
    
    enemy = Pokemon(names[random_index[0]], enemy_images[0], urls[random_index[0]], random_index[0])
    details_about_enemy = enemy.get_details(enemy.id)


    return render(request, 'aplication/fights1.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2],
                                                        'enemy': enemy, 'hp_enemy': details_about_enemy[0], 'attack_enemy': details_about_enemy[1], 'speed_enemy': details_about_enemy[2],
                                                        })

def fights1(request, name, enemy_name):
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


    enemy_names = [name for name in names if name.lower().startswith(enemy_name.lower())]
    indexes = [index for index, name in enumerate(names) if name in enemy_names]
    random_index = [index+1 for index in indexes]


    # random_index = [random.randint(1, counts-1)]
    enemy_images = display_images_serach(random_index)
    
    enemy = Pokemon(names[random_index[0]], enemy_images[0], urls[random_index[0]], random_index[0])
    details_about_enemy = enemy.get_details(enemy.id)

    hp = details_about[0]
    attack = details_about[1]
    hp_enemy = details_about_enemy[0]
    attack_enemy = details_about_enemy[1]

    date = datetime.now().date()
    time = datetime.now().time()
    win_id = 0

    if request.method == 'POST':
        number_user = (int)(request.POST.get("hit"))
        number_enemy = random.randint(1, 10)
        round_сol = 0
        result = 'ooo'

        if ((number_user%2==1 and number_enemy%2==1) or (number_user%2==0 and number_enemy%2==0)):
            while (hp_enemy > 0 and hp > 0):
                hp_enemy = hp_enemy - attack
                if (hp_enemy > 0):
                    hp = hp - attack_enemy
                    if (hp < 0):
                        result = 'Выйграл противник'
                        win_id = enemy.id
                else:
                    result = 'Выйграл ты'
                    win_id = pokemon_list[0].id
                round_сol += 1
            fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy.id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy.id))
            fight.save()
            # send(fight)
            return render(request, 'aplication/fights.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2],
                                                        'enemy': enemy, 'hp_enemy': details_about_enemy[0], 'attack_enemy': details_about_enemy[1], 'speed_enemy': details_about_enemy[2],
                                                        'result':result, 'name': pokemon_list[0].name, 'enemy_name': enemy.name, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})
        else:
            while (hp_enemy > 0 and hp > 0):
                hp = hp - attack_enemy
                if (hp > 0):
                    hp_enemy = hp_enemy - attack
                    if (hp_enemy < 0):
                        result = 'Выйграл ты'
                        win_id = pokemon_list[0].id
                else:
                    result = 'Выйграл противник'
                    win_id = enemy.id
                round_сol += 1
            fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy.id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy.id))
            fight.save()
            # send(fight)
            return render(request, 'aplication/fights.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2],
                                                        'enemy': enemy, 'hp_enemy': details_about_enemy[0], 'attack_enemy': details_about_enemy[1], 'speed_enemy': details_about_enemy[2],
                                                        'result':result, 'name': pokemon_list[0].name, 'enemy_name': enemy.name, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})


def fastfights(request, name):
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

    random_index = [random.randint(1, counts-1)]
    enemy_images = display_images_serach(random_index)
    
    enemy = Pokemon(names[random_index[0]], enemy_images[0], urls[random_index[0]], random_index[0])
    details_about_enemy = enemy.get_details(enemy.id)


    hp = details_about[0]
    attack = details_about[1]
    hp_enemy = details_about_enemy[0]
    attack_enemy = details_about_enemy[1]

    date = datetime.now().date()
    time = datetime.now().time()
    win_id = 0
    number_user = random.randint(1, 10)
    number_enemy = random.randint(1, 10)
    round_сol = 0
    result = 'ooo'

    if ((number_user%2==1 and number_enemy%2==1) or (number_user%2==0 and number_enemy%2==0)):
        while (hp_enemy > 0 and hp > 0):
            hp_enemy = hp_enemy - attack
            if (hp_enemy > 0):
                hp = hp - attack_enemy
                if (hp < 0):
                    result = 'Выйграл противник'
                    win_id = enemy.id
            else:
                result = 'Выйграл ты'
                win_id = pokemon_list[0].id
            round_сol += 1
        fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy.id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy.id))
        fight.save()
        # send(fight)
        return render(request, 'aplication/fast_fight.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2],
                                                      'enemy': enemy, 'hp_enemy': details_about_enemy[0], 'attack_enemy': details_about_enemy[1], 'speed_enemy': details_about_enemy[2],
                                                      'result':result, 'name': pokemon_list[0].name, 'enemy_name': enemy.name, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})
    else:
        while (hp_enemy > 0 and hp > 0):
            hp = hp - attack_enemy
            if (hp > 0):
                hp_enemy = hp_enemy - attack
                if (hp_enemy < 0):
                    result = 'Выйграл ты'
                    win_id = pokemon_list[0].id
            else:
                result = 'Выйграл противник'
                win_id = enemy.id
            round_сol += 1
        fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy.id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy.id))
        fight.save()
        
        
        # send(fight)
        

        return render(request, 'aplication/fast_fight.html', {'Pokemon': pokemon_list[0], 'hp': details_about[0], 'attack': details_about[1], 'speed': details_about[2],
                                                      'enemy': enemy, 'hp_enemy': details_about_enemy[0], 'attack_enemy': details_about_enemy[1], 'speed_enemy': details_about_enemy[2],
                                                      'result':result, 'name': pokemon_list[0].name, 'enemy_name': enemy.name, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})

def send(fight):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)

    server.starttls()

    server.login('', '')

    # Создаем письмо
    msg = MIMEText('Бой №' + str(fight.fightid) + '\n Прошел ' + str(fight.date) + ' в ' + str(fight.time) + '\n Между ' + str(fight.poke_id) + ' и ' + str(fight.enemy_id) + '.')
    msg['Subject'] = 'Победил покемон №' + str(fight.win_id)
    msg['From'] = ''
    msg['To'] = ''

    server.sendmail('', [''], msg.as_string())
    server.quit()
    


def send_result(request):
    return render(request, 'aplication/message.html', {})
