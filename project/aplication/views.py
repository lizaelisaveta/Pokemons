from email.mime import image
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Fight
from .models import Pokemon
import requests
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText


# BASE_URL = 'https://pokeapi.co/api/v2/pokemon'

# def get_details(id):
#     response = requests.get(f"{BASE_URL}/{id}").json()
#     hp = response['stats'][0]['base_stat']
#     attack = response['stats'][1]['base_stat']
#     speed = response['stats'][-1]['base_stat']
#     name = response['name']
#     url = response['abilities']['ability']['url']
#     image = display_images_serach(id)
#     arrays = [hp, attack, speed, name, url, image]
#     return arrays

# # def download_pokemons():
# #     count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
# #     count_poke_json = count.json()
# #     counts = count_poke_json['count']
# #     # name_poke = requests.get('https://pokeapi.co/api/v2/pokemon?limit=' + str(counts) + '&offset=0')
# #     # name_poke_json = name_poke.json()
# #     # names = [result['name'] for result in name_poke_json['results']]
# #     # urls = [result['url'] for result in name_poke_json['results']]

# #     # indexes = [index for index, name in enumerate(names) if name in names]
# #     # indexes = [index+1 for index in indexes]
    
# #     # images = display_images_serach(indexes)
    
# #     # pokemon_data = [[name for name in names], [image for image in images],[url for url in urls], [ind for ind in indexes] ]
# #     # pokemon_list = [(name, image,url,id) for name, image, url,id in zip(*pokemon_data)]

# #     for i in range(counts):
# #         details_about = get_details(i)
# #         poke = Pokemon(i, details_about[3], details_about[4], details_about[5], details_about[0], details_about[1], details_about[2])
# #         poke.save()


# # def list_names1(request):
# #     download_pokemons()



def list_names(request):
    query = ''
    if 'search_query' in request.session:
        query = request.session['search_query']
        
    if request.GET.get('query'):
        query = request.GET.get('query')
        request.session['search_query'] = query

    pokemon_list = Pokemon.objects.all()
    
    count_pages = 20
    paginator = Paginator(pokemon_list, count_pages)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list, 'counts': pokemon_list.count, 'paginator': paginator, 'page_obj': page_obj, 'query': query}) #


def search_results(request):
    query = ''
    if 'search_query' in request.session:
        query = request.session['search_query']
        
    if request.GET.get('query'):
        query = request.GET.get('query')
        request.session['search_query'] = query

    pokemon_list = Pokemon.objects.filter(name__startswith=str(query))
    
    count_pages = 20
    paginator = Paginator(pokemon_list, count_pages)
    
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list,'counts': pokemon_list.count, 'paginator':paginator, 'page_obj': page_obj, 'query': query})


def details(request, id):
    pokemon_list = Pokemon.objects.filter(id=id)
    
    return render(request, 'aplication/details.html', {'Pokemon': pokemon_list[0]})


def fights(request, id):
    pokemon_list = Pokemon.objects.filter(id=id)
    
    random_index = random.randint(1, 1016)
    enemy = Pokemon.objects.filter(id=int(random_index))

    return render(request, 'aplication/fights1.html', {'Pokemon': pokemon_list[0], 'enemy': enemy[0]})


def fights1(request, id, enemy_id):
    pokemon_list = Pokemon.objects.filter(id=id)
    enemy = Pokemon.objects.filter(id=enemy_id)

    hp = pokemon_list[0].hp
    attack = pokemon_list[0].attack
    hp_enemy = enemy[0].hp
    attack_enemy = enemy[0].attack

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
                        win_id = enemy[0].id
                else:
                    result = 'Выйграл ты'
                    win_id = pokemon_list[0].id
                round_сol += 1
            fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy[0].id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy[0].id))
            fight.save()
            # send(fight)
            return render(request, 'aplication/fights.html', {'Pokemon': pokemon_list[0], 'enemy': enemy, 'result':result, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})
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
                    win_id = enemy[0].id
                round_сol += 1
            fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy[0].id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy[0].id))
            fight.save()
            # send(fight)
            return render(request, 'aplication/fights.html', {'Pokemon': pokemon_list[0], 'enemy': enemy[0], 'result':result, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})


def fastfights(request, id):
    pokemon_list = Pokemon.objects.filter(id=id)
    random_index = random.randint(1, 1016)
    enemy = Pokemon.objects.filter(id=int(random_index))
    
    hp = pokemon_list[0].hp
    attack = pokemon_list[0].attack
    hp_enemy = enemy[0].hp
    attack_enemy = enemy[0].attack

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
                    win_id = enemy[0].id
            else:
                result = 'Выйграл ты'
                win_id = pokemon_list[0].id
            round_сol += 1
        fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy[0].id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy[0].id))
        fight.save()
        # send(fight)
        return render(request, 'aplication/fast_fights.html', {'Pokemon': pokemon_list[0], 'enemy': enemy, 'result':result, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})
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
                win_id = enemy[0].id
            round_сol += 1
        fight = Fight(int(win_id)+int(pokemon_list[0].id)+int(enemy[0].id),date,time,str(win_id),str(pokemon_list[0].id),str(enemy[0].id))
        fight.save()
        # send(fight)
        return render(request, 'aplication/fast_fights.html', {'Pokemon': pokemon_list[0], 'enemy': enemy[0], 'result':result, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})


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
