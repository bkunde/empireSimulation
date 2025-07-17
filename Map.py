#Map.py 

import random
import settings
import Hex
import BasicTiles

class Map:
    def __init__(self):
        self.wheatTiles = self.getWheatTiles() 

    def update(self):
        self.checkWheat()


    def checkWheat(self):   
        for tile in self.wheatTiles:
            if tile.tile_type.amount <= 0:
                tile.setTile(BasicTiles.Barren(tile.q, tile.r, 'barren'))
                self.wheatTiles.remove(tile)
    
    def getWheatTiles(self):
        wheat = []
        for row in settings.HEX_MAP.tiles:
            for tile in row:
                if tile.tile_type.name == 'wheat':
                    wheat.append(tile)

        return wheat

    def getNeighbors(self, tile):
        neighbors = []
        for i in range(6):
            q, r = Hex.hex_neighbor(tile.q, tile.r, i)
            
            if (0 <= r < len(settings.HEX_MAP.tiles) and 0 <= q < len(settings.HEX_MAP.tiles[r])):
                neighbors.append(settings.HEX_MAP.tiles[r][q])

        return neighbors
            
                    
    def generateLakes(self, count=5, lake_size=6):
        all_tiles = [tile for row in settings.HEX_MAP.tiles for tile in row]
        
        for i in range(count):
            center = random.choice(all_tiles)
            lake_tiles = set()
            lake_tiles.add(center)

            frontier = [center]
            while len(lake_tiles) < lake_size and frontier:
                tile = frontier.pop()
                neighbors = self.getNeighbors(tile)
                random.shuffle(neighbors)
                for neighbor in neighbors:
                    if len(lake_tiles) >= lake_size:
                        break
                    lake_tiles.add(neighbor)
                    frontier.append(neighbor)

            for tile in lake_tiles:
                waterTile = BasicTiles.Water(tile.q, tile.r, 'water', 'lake', passable=False)
                tile.setTile(waterTile)
                
    
    def generateRivers(self, start_tile, max_length=20):
        current = start_tile
        path = [current]
        
        for i in range(max_length):
            neighbors = self.getNeighbors(current)
            grass_neighbors = [n for n in neighbors if n.tile_type.name == 'grass']
            if not grass_neighbors:
                break
            
            grass_neighbors.sort(key=lambda t: t.q + t.r + random.random())
            next_tile = grass_neighbors[0]
            path.append(next_tile)
            current = next_tile
            
        for tile in path:
            waterTile = BasicTiles.Water(tile.q, tile.r, 'water', 'river',  passable=False)
            tile.setTile(waterTile)
            
            
                

    def generateMap(self, seed=None):
        if seed is not None:
            random.seed(seed)

        waterTiles = []
        grassTiles = []
        mountainTiles = []
        terrains = ['grass', 'water', 'mountain']
        for row in settings.HEX_MAP.tiles:
            for tile in row:
                terrain = random.choices(terrains, weights=[0.9,0.0,0.1],k=1)[0]
                if terrain == 'grass': 
                    tileType = BasicTiles.Grass(tile.q, tile.r, terrain)
                    grassTiles.append(tile)
                #elif terrain == 'water': tileType = BasicTiles.Water(tile.q, tile.r, terrain, passable=False)
                elif terrain == 'mountain': 
                    tileType = BasicTiles.Mountain(tile.q, tile.r, terrain, passable=False)
                    mountainTiles.append(tile)
                else:
                    tileType=BasicTiles.Barren(tile.q, tile.r, 'barren')

                tile.setTile(tileType)
                
                
        for i in range(random.randint(1, 5)):
            self.generateRivers(random.choice(mountainTiles), max_length=20)

        self.generateLakes(count=random.randint(2,8), lake_size=random.randint(3,10))


        
    
