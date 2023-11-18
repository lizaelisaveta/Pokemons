from django.test import TestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service
import unittest
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page(self):
        response = self.client.get(reverse('list_names'))
        self.assertEqual(response.status_code, 200)

    # def test_pokemon(self):
    #     response = self.client.get('/detail/1/')
    #     self.assertEqual(response.status_code, 200)

    # def test_fight(self):
    #     response = self.client.get('/fights/1/')
    #     self.assertEqual(response.status_code, 200)

    # def test_search(self):
    #     response = self.client.post('/search', {'search': 'pikachu'})
    #     self.assertEqual(response.status_code, 200)


class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        # self.driver = webdriver.Chrome('chromedriver.exec')
        # self.driver = webdriver.Safari()
        # chrome_driver_path = '/Users/doit/Documents/GitHub/Pokemons/project/chromedriver'
        # driver = webdriver.Chrome(chrome_driver_path)
        self.driver = webdriver.Chrome(executable_path='/Users/doit/Downloads/chromedriver')

    def test_page(self):
        self.driver.get('http://localhost:8000/')
        self.assertIn('Pokemons', self.driver.title)
        pokemon_list = self.driver.find_element_by_class_name('card')
        self.assertTrue(pokemon_list.is_displayed())

    # def test_pokemon(self):
    #     self.driver.get('http://localhost:8000/detail/1/')
    #     self.assertIn('Pokemon Details', self.driver.title)
    #     pokemon_info = self.driver.find_element_by_class_name('card-about')
    #     self.assertTrue(pokemon_info.is_displayed())

    # def test_search(self):
    #     self.driver.get('http://localhost:8000/')
    #     search_input = self.driver.find_element_by_id('search-string')
    #     search_input.send_keys('pikachu')
    #     search_button = self.driver.find_element_by_id('search-button')
    #     search_button.click()
    #     search_results = self.driver.find_element_by_class_name('card')
    #     self.assertTrue(search_results.is_displayed())

    # def test_fight(self):
    #     self.driver.get('http://localhost:8000/detail/1/')
    #     choose_button = self.driver.find_element(By.XPATH, '//button[text()="Выбрать для обычного боя!"]')
    #     choose_button.click()
    #     search_input = self.driver.find_element_by_id('form-control')
    #     search_input.send_keys('2')
    #     attack_button = self.driver.find_element(By.XPATH, '//button[value()="В бой!"]')
    #     attack_button.click()
    #     player_turn = self.driver.find_element_by_class_name('send_on_email')
    #     self.assertTrue(player_turn.is_displayed())
