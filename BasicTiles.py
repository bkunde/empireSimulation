#Grass.py

from Tile import Tile

class Grass(Tile):
    def __init__(self, q, r, name, color):
        super().__init__(q, r, name, color)

class Barren(Tile):
    def __init__(self, q, r, name, color):
        super().__init__(q, r, name, color)

class Mountain(Tile):
    def __init__(self, q, r, name, color, passable=False):
        super().__init__(q, r, name, color)

class Water(Tile):
    def __init__(self, q, r, name, color, waterType='river', passable=False):
        super().__init__(q, r, name, color)
        self.waterType = waterType
