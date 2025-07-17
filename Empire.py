#country.py

import settings
import pygame
import Citizen

class Empire:
    #Countries are made up of n number of citizens
    #each country is represented by a color

    def __init__(self, color):
        self.color = color
        self.citizens = []

    def createCitizens(self):
        citizen = Citizen.Citizen(self.color, settings.randomPosition())
        self.citizens.append(citizen)

    
