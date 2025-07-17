#city.py
import settings
import pygame
from Tile import Tile
import Citizen

class City(Tile):
    def __init__(self, q, r, name, country=None):
        super().__init__(q, r, name, country.color)
        self.country = country
        self.citizens = []
        self.growAmount = 2
        self.resources = {'wheat': self.growAmount}
        
    def update(self):
        #check resources
        if self.resources['wheat'] >= self.growAmount:
            self.grow()

    def grow(self):
        self.resources['wheat'] -= self.growAmount
        self.spawnNewCitizen()
    
    def spawnNewCitizen(self):
        spawn_pos = pygame.Vector2(self.pixelX, self.pixelY)
        new_citizen = Citizen.Citizen(self.country.color, spawn_pos, self, 'farmer')
        self.citizens.append(new_citizen)
        print(f"{self.name} has grown! Population: {len(self.citizens)}")

    def addResource(self, resource):
        if resource in self.resources:
            self.resources[resource] += 1
        else:
        
            self.resources[resource] = 1
        print(self.resources)



 
