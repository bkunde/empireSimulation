#Grass.py

from Tile import Tile

class Grass(Tile):
    def __init__(self, q, r, name):
        super().__init__(q, r, name)

class Barren(Tile):
    def __init__(self, q, r, name):
        super().__init__(q, r, name)

class Mountain(Tile):
    def __init__(self, q, r, name, passable=False):
        super().__init__(q, r, name)

class Water(Tile):
    def __init__(self, q, r, name, waterType='river', passable=False):
        super().__init__(q, r, name)
        self.waterType = waterType
