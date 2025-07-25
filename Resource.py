#Resource.py

from Tile import Tile

class Resource(Tile):
    def __init__(self, q, r, name, color, amount):
        super().__init__(q, r, name, color, amount=amount)

    def harvest(self):
        if self.amount > 0:
            self.amount -= 1

