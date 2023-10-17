from datetime import date
from time import time
from unittest import result
from django.conf import settings
from django.db import models
from django.utils import timezone


class Fight(models.Model):
    fightid = models.IntegerField(db_column='FightId', primary_key=True)
    date = models.DateField(db_column='Date')
    time = models.TimeField(db_column='Time')
    win_id = models.ImageField(db_column='WinnerId')
    poke_id = models.ImageField(db_column='PokeId')
    enemy_id = models.ImageField(db_column='EnemyId')
    def __str__(self):
        return str(self.fightid)
    class Meta:
        db_table = 'fights'


class Pokemon(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)
    name = models.CharField(db_column='Name')
    url = models.CharField(db_column='Url')
    image = models.CharField(db_column='Image')
    hp = models.IntegerField(db_column='Hp')
    attack = models.IntegerField(db_column='Attack')
    speed = models.IntegerField(db_column='Speed')

    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'pokemons'
    
