from email.mime import image
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Fight
from .models import Pokemon
import requests
from django.contrib.auth.models import User
from datetime import datetime
import string
import random
import os
import smtplib
import secrets
import uuid
from email.mime.text import MIMEText
from django.contrib.auth.decorators import login_required
import json
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
import redis
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from aplication.forms import RegisterForm



redis_client = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)


def get_pokemons(page):
    key = 'pokemons_{}'.format(page)
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    
    pokemons = Pokemon.objects.all().order_by('id')[(int(page) - 1) * 20: int(page) * 20]
    data = []
    for pokemon in pokemons:
        data.append({
            'name': pokemon.name,
            'id': pokemon.id,
            'image': pokemon.image
        })
    redis_client.setex(key, 3600, json.dumps(data))

    return data


def list_names(request):    
    query = ''
    if 'search_query' in request.session:
        query = request.session['search_query']
        
    if request.GET.get('query'):
        query = request.GET.get('query')
        request.session['search_query'] = query
  
    count_pages = 20
    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1
    
    all_data = Pokemon.objects.all()
    
    key = 'pokemon_{}'.format(page_number)
    data = redis_client.get(key)
    if data:
        pokemon_list = json.loads(data)
    else:
        pokemon_list = get_pokemons(page_number)
        
    paginator = Paginator(all_data, count_pages)
    
    page_obj = paginator.get_page(page_number)
    page_obj.object_list = pokemon_list

    return render(request, 'aplication/list_names.html', {'pokemon_list': page_obj.object_list, 'counts': Pokemon.objects.all().count, 'paginator': paginator, 'page_obj': page_obj, 'query': query})


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
            fight = Fight(date=date,time=time,win_id=str(win_id),poke_id=str(pokemon_list[0].id),enemy_id=str(enemy[0].id), userid=get_id_active_user(request))
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
            fight = Fight(date=date,time=time,win_id=str(win_id),poke_id=str(pokemon_list[0].id),enemy_id=str(enemy[0].id), userid=get_id_active_user(request))
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
        fight = Fight(date=date,time=time,win_id=str(win_id),poke_id=str(pokemon_list[0].id),enemy_id=str(enemy[0].id), userid=get_id_active_user(request))
        fight.save()
        # send(fight, request.user.email)
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
        fight = Fight(date=date,time=time,win_id=str(win_id),poke_id=str(pokemon_list[0].id),enemy_id=str(enemy[0].id), userid=get_id_active_user(request))
        fight.save()
        # send(fight, request.user.email)
        return render(request, 'aplication/fast_fights.html', {'Pokemon': pokemon_list[0], 'enemy': enemy[0], 'result':result, 'round':round_сol, 'num_us':number_user, 'en_num':number_enemy})


def get_id_active_user(request):
    if request.user.is_authenticated:
        return request.user.id
    else:
        return 0


def send_result(request):

    return render(request, 'aplication/message.html', {})


def save_doc_about(request, id):
    pokemon_list = Pokemon.objects.filter(id=id)[0]
    date = datetime.now().date()
    
    folder_path = "/Users/liza/Documents/Pokemons/"

    folder_name = str(date)

    if not os.path.exists(folder_path + folder_name):
        os.makedirs(folder_path + folder_name)

    file_path = os.path.join(folder_path + folder_name, str(pokemon_list.name) + '.md')
    
    with open(file_path, "w") as file:
        file.write(f"# Pokemon {pokemon_list.name}\n\n")
        file.write(f"Hp: **{pokemon_list.hp}**\n")
        file.write(f"Attack: **{pokemon_list.attack}**\n")
        file.write(f"Speed: **{pokemon_list.speed}**\n")
        file.write(f"![{pokemon_list.name}]({pokemon_list.image})\n")

    return render(request, 'aplication/savedoc.html', {})


BASE_URL = 'https://pokeapi.co/api/v2/pokemon'


def display_images_serach(indexes):
    if indexes:
        pokeImages = []
        for i in indexes:
            pokeID = i
            pokeImage = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokeID}.png"
            pokeImages.append(pokeImage)
        return  pokeImages[0]
    pokeImage = "https://img.icons8.com/color/96/pokeball--v1.png"
    return  pokeImage


def get_details(id):
    response = requests.get(f"{BASE_URL}/{id}").json()
    hp = response['stats'][0]['base_stat']
    attack = response['stats'][1]['base_stat']
    speed = response['stats'][-1]['base_stat']
    name = response['name']
    url = response['abilities']['ability']['url']
    image = display_images_serach(id)
    arrays = [hp, attack, speed, name, url, image]
    return arrays

def download_pokemons(request):
    count = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1&offset=0')
    count_poke_json = count.json()
    counts = count_poke_json['count']
    db = Pokemon.objects.all

    for i in range(counts):
        details_about = get_details(i)
        poke = Pokemon(i, details_about[3], details_about[4], details_about[5], details_about[0], details_about[1], details_about[2])
        if db.objects.filter(id=poke.id, name=poke.name).exists():
            continue
        else:
            poke.save()
            
    return redirect('list_names', request)


def send(fight, to_email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    msg = MIMEText('Бой' + '\n прошел ' + str(fight.date) + ' в ' + str(fight.time) + '\n Между ' + str(fight.poke_id) + ' и ' + str(fight.enemy_id) + '.')
    msg['Subject'] = 'Победил покемон №' + str(fight.win_id)
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email
    server.sendmail(settings.EMAIL_HOST_USER, [to_email], msg.as_string())
    server.quit()


def send_mails(subject, message, from_email, to_email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()


@login_required
def profile(request):
    return render(request, 'aplication/profile.html')


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user, created = User.objects.get_or_create(email=form.cleaned_data["email"])
        new_pass = None

        if created:
            alphabet = string.ascii_letters + string.digits
            new_pass = ''.join(secrets.choice(alphabet) for i in range(8))
            user.set_password(new_pass)
            user.save(update_fields=["password", ])

        if new_pass or user.is_active is False:
            token = uuid.uuid4().hex
            redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
            cache.set(redis_key, {"user_id": user.id}, timeout=settings.USER_CONFIRMATION_TIMEOUT)

            confirm_link = self.request.build_absolute_uri(
                reverse_lazy(
                    "register_confirm", kwargs={"token": token}
                )
            )
            message = (f"follow this link %s \n"
                        f"to confirm! \n" % confirm_link)
            if new_pass:
                message += f"Your new password {new_pass} \n "

            send_mails("Please confirm your registration!", message, settings.EMAIL_HOST_USER, user.email)
        return super().form_valid(form)


def register_confirm(request, token):
    redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
    useer_info = cache.get(redis_key) or {}

    if user_id := useer_info.get("user_id"):
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save(update_fields=["is_active"])
        return redirect(to=reverse_lazy("profile"))
    else:
        return redirect(to=reverse_lazy("register"))


