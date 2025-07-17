#map.py
#https://www.redblobgames.com/grids/hexagons/#line-drawing
import pygame
import settings
import BasicTiles 
import Map
import math

class HexTile:
    def __init__(self, q, r, size=30, tile_type=None):
        self.q = q
        self.r = r
        self.size = size
        self.tile_type = tile_type
        self.color = None
        self.pixelX = 0
        self.pixelY = 0
        self.highlighted = False

    def get_color(self):
        match self.tile_type.name:
            case "grass": return (34,139,34)
            case "water": 
                if self.tile_type.waterType == 'river': return (2,117,255)
                elif self.tile_type.waterType == 'lake': return (2, 64, 255)
            case "mountain": return (105,105,105)
            case "wheat": return(241,231,52)
            case "city": return (255,0,0) #self.tile_type.color
            case "barren": return(64,48,38)
            case _: return (200,200,200)
            

    def setTile(self, tile):
        self.tile_type = tile
        self.color = tile.color #self.get_color()


    def get_hex_points(self):
        points = []
        for angle in range(30, 360, 60):
            points.append((
                self.pixelX+self.size * math.cos(math.radians(angle)),
                self.pixelY+self.size * math.sin(math.radians(angle))))
    
        return points
            

    def draw(self):
        points = self.get_hex_points()
        pygame.draw.polygon(settings.SCREEN, self.color, points) #fill
        if self.highlighted:
            pygame.draw.polygon(settings.SCREEN, (255,0,190), points, 3) #border
        else:
            pygame.draw.polygon(settings.SCREEN, (0,0,0), points, 1) #border

    def __str__(self):
        if self.tile_type.name == 'grass' or self.tile_type.name == 'wheat':
            return f"<Hex at {(self.q, self.r)}, Tile = {self.tile_type.name}, Fertility = {self.tile_type.fertility}>"
        else:
            return f"<Hex at {(self.q, self.r)}, Tile = {self.tile_type.name}>" 

class HexMap:
    #map is a grid of hex tiles
    #using an axial coordinate system where s = -q-r
    def __init__(self, size=30):
        self.max_radius = 12
        self.tiles = [[None]]*(self.max_radius*2+1)
    
        for i in range(len(self.tiles)):
            self.tiles[i] = [None]*((2*self.max_radius+1) - abs(self.max_radius-i))

        for q, r in generate_hex_grid(self.max_radius):
            grassTile = BasicTiles.Grass(q, r, 'grass', (0,0,0))
            tile = HexTile(q, r, size, tile_type = grassTile)
            tile.pixelX, tile.pixelY = axial_to_pixel(q, r, size)
            self.tiles[r][q - max(0, self.max_radius-r)] = tile

    def draw(self):
        for row in self.tiles:
            for tile in row:
                tile.draw()
    
    def getRadius(self):
        return self.max_radius


### HELPER FUNCTIONS ###


HEX_DIRECTIONS = [ (1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1) ]
#start hex starts in center of the screen
START_HEX_PIXEL = settings.WIDTH // 2, settings.HEIGHT // 2

def hex_neighbor(q, r, direction):
    dq, dr = HEX_DIRECTIONS[direction]   
    return (q + dq, r+dr)

def generate_hex_grid(max_radius):
    tiles = [(max_radius, max_radius)] #start with (q,r) in the center
    
    for radius in range(1, max_radius+1):
        q,r = max_radius-radius, max_radius+radius
        for i in range(6):
            for j in range(radius):
            #moving out and starting with norteast
                q,r = hex_neighbor(q,r,i)
                tiles.append((q,r))
    return tiles
        
def generate_hex_spiral(size):
    centerX = settings.WIDTH // 2
    centerY = settings.HEIGHT // 2
    seen = set()
    tiles = [] 

    max_radius = 50

    for radius in range(max_radius):
        if radius == 0:
            q, r  = 0, 0 
            x, y = axial_to_pixel(q, r, size, centerX, centerY)
            if 0 <= x <= settings.WIDTH and 0 <= y <= settings.HEIGHT:
                tiles.append((q,r))

        else:
            q, r = -radius, radius
            for i in range(6):
                for j in range(radius):
                    if (q,r) not in seen:
                        x, y = axial_to_pixel(q, r, size, centerX, centerY)
                        if 0 <= x <= settings.WIDTH and 0 <= y <= settings.HEIGHT:
                            tiles.append((q,r))
                            seen.add((q,r))
                    q, r = hex_neighbor(q, r, i)

    return tiles


def axial_to_pixel(q, r, size):
    #convert axial coords to pixel coords
    x = (math.sqrt(3) * q + math.sqrt(3)/2 * r) 
    y = (3/2 * r) 
    
    #scale cartesian coords
    x = (x) * size
    y = (y) * size

    #adjust to center on screen
    #x += settings.WIDTH//2-size
    #y += settings.HEIGHT//2-size
    return (x, y)

def pixel_to_axial(point, size=10): #point = pygame.Vector2
    #invert scaling
    x = point.x / size
    y = point.y / size
    #x = x / size
    #y = y / size

    #cartesian to hex
    q = math.sqrt(3)/3 * x - (1/3) * y
    r = 2/3 * y
    return (q,r)

def axial_distance(a, b):
    return(abs(a.q - b.q)
        + abs(a.q + a.r - b.q - b.r)
        + abs(a.r - b.r) / 2)
    

def closestTile(current_tile, goal):
    tiles = []
    for row in settings.HEX_MAP.tiles:
        for tile in row:
            if tile.tile_type.name == goal:
                tiles.append(tile)

    closestTile = None
    for tile in tiles:
        dist = 100
        current_distance = axial_distance(current_tile, tile)
        if current_distance <= dist:
            dist = current_distance
            closestTile = tile 

    return closestTile

