from django.test import TestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from .models import Pokemon


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page(self):
        response = self.client.get(reverse('list_names'))
        self.assertEqual(response.status_code, 200)
        pokemon_list = response.context['pokemon_list']
        self.assertEqual(len(pokemon_list), 20)
        self.assertEqual(pokemon_list[0]['name'], "bulbasaur")

    def test_pokemon(self):
        self.assertEqual(len(Pokemon.objects.all()), 0)
        pok = Pokemon.objects.create(hp = 100, attack = 20, speed = 20,url = "urenfrn", name = 'bulbasaur', id = 1, image = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png')
        response = self.client.get(reverse('details', args=[int(1)]))
        self.assertEqual(response.status_code, 200)
        pokemon_= response.context['Pokemon']
        self.assertEqual(pokemon_.name, "bulbasaur")

    def test_fight(self):
        self.assertEqual(len(Pokemon.objects.all()), 0)
        pok = Pokemon.objects.create(hp = 100, attack = 20, speed = 20,url = "urenfrn", name = 'bulbasaur', id = 1, image = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png')
        pok1 = Pokemon.objects.create(hp = 120, attack = 10, speed = 20,url = "urenfrn", name = 'venusaur', id = 2, image = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/2.png')

        response = self.client.get(reverse('fastfights', args=[int(1)]))
        pokemon_list = response.context['Pokemon']
        self.assertEqual(pokemon_list.name, "bulbasaur")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(Pokemon.objects.all()), 2)
        self.assertTemplateUsed(response, 'aplication/fast_fights.html')


class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        super().setUpClass()
        self.driver = WebDriver()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_page(self):
        self.driver.get('http://localhost:8000/')
        self.assertIn('Pokemons', self.driver.title)
        pokemon_list = self.driver.find_element(By.CLASS_NAME, "card")

        self.assertTrue(pokemon_list.is_displayed())

    def test_pokemon(self):
        self.driver.get('http://localhost:8000/detail/1/')
        self.assertIn('Pokemon Details', self.driver.title)
        pokemon_info = self.driver.find_element(By.CLASS_NAME, 'card-about')
        self.assertTrue(pokemon_info.is_displayed())

    def test_search(self):
        self.driver.get('http://localhost:8000/')
        search_input = self.driver.find_element(By.NAME, 'query')
        search_button = self.driver.find_element(By.XPATH, "/html/body/div/div/form/button")
        search_input.send_keys('pikachu')
        search_button.click()
        search_results = self.driver.find_element(By.CLASS_NAME, "card")
        self.assertTrue(search_results.is_displayed())

    def test_fight(self):
        self.driver.get('http://localhost:8000/detail/1/')
        choose_button = self.driver.find_element(By.NAME, "button_my")
        choose_button.click()
        search_input = self.driver.find_element(By.CLASS_NAME, 'form-control')
        search_input.send_keys('2')
        attack_button = self.driver.find_element(By.NAME, 'but_attack')
        attack_button.click()
        player_turn = self.driver.find_element(By.NAME, 'sends')
        self.assertTrue(player_turn.is_displayed())