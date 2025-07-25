#Tile.py

import pygame
import settings
import Hex

class Tile:
    def __init__(self, q, r, name, color, amount=0, passable=True, resource=None):
        self.q = q
        self.r = r
        self.name = name
        self.color = color
        self.fertility = 0.0
        self.amount = amount
        self.passable = passable
        self.resource = resource
        self.pixelX, self.pixelY = Hex.axial_to_pixel(q,r,10)
        self.claimed_by = set()
        
