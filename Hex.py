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
        self.color = (200,200,200)
        self.pixelX = 0
        self.pixelY = 0
        self.highlighted = False

    def get_color(self):
        """
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
        """ 

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

        self.map_width = int(settings.WIDTH // (math.sqrt(3) * size)) #cols
        self.map_height = int(settings.HEIGHT // (1.5 * size))        #rows
        
        self.tiles = [[None for _ in range(self.map_width)] for _ in range(self.map_height)]
        for r in range(self.map_height):
            row_offset = r//2
            for col in range(self.map_width):
                q = col - row_offset
                defaultTile = BasicTiles.Barren(q, r, 'barren', (0,0,0))
                tile = HexTile(q, r, size, tile_type = defaultTile)
                tile.pixelX, tile.pixelY = axial_to_pixel(q, r, size)
                self.tiles[r][col] = tile
        
        #self.tiles = [None for _ in range(self.max_radius * 2 +1)] #[[None]]*(self.max_radius*2+1)
        """    
        for i in range(len(self.tiles)):
            self.tiles[i] = [None]*((2*self.max_radius+1) - abs(self.max_radius-i))

        for q, r in generate_hex_grid_rectangle():#generate_hex_grid_hexagon(self.max_radius):
            defaultTile = BasicTiles.Barren(q, r, 'barren', (0,0,0))
            
            tile = HexTile(q, r, size, tile_type = defaultTile)
            tile.pixelX, tile.pixelY = axial_to_pixel(q, r, size)
            self.tiles[0].append(tile)
            self.tiles[r][q - max(0, self.max_radius-r)] = tile
            """
            

    def getTile(self, q, r):
        col = q + (r // 2)
        if 0 <= r < self.map_height and 0 <= col < self.map_width:
            return self.tiles[r][col]
        return None

    def draw(self):
        for row in self.tiles:
            for tile in row:
                tile.draw()
    
    def getRadius(self):
        return self.max_radius


### HELPER FUNCTIONS ###


HEX_DIRECTIONS = [ (1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1) ]

#directions in e, ne, nw, w, sw, se
ODD_R_OFFSETS = {
    0: [(1,0), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)], #even rows
    1: [(1,0), (1,-1), (0,-1), (-1,0), (0,1), (1,1)]    #odd rows
}
#start hex starts in center of the screen
START_HEX_PIXEL = settings.WIDTH // 2, settings.HEIGHT // 2

#returns a single tile based on direction
def hex_neighbor(q, r, direction):
    parity = r % 2
    dq, dr = ODD_R_OFFSETS[parity][direction]
    return (q + dq, r+dr)
    """
    dq, dr = HEX_DIRECTIONS[direction]   
    return (q + dq, r+dr)
    """
    
#returns a list of all neighbor tiles
def get_neighbors(q, r):
    neighbors = []
    for dq, dr in HEX_DIRECTIONS:
        nq, nr = q+dq, r+dr
        neighbor_tile = settings.HEX_MAP.getTile(nq, nr)
        if neighbor_tile:
            neighbors.append(neighbor_tile)
    return neighbors

def generate_hex_grid_hexagon(max_radius):
    tiles = [(max_radius, max_radius)] #start with (q,r) in the center
    
    for radius in range(1, max_radius+1):
        q,r = max_radius-radius, max_radius+radius
        for i in range(6):
            for j in range(radius):
            #moving out and starting with norteast
                q,r = hex_neighbor(q,r,i)
                tiles.append((q,r))
    return tiles

def axial_to_pixel(q, r, size):
    #convert axial coords to pixel coords
    x = math.sqrt(3) * q + (math.sqrt(3)/2 * r) 
    y = (3/2 * r) 
    
    #scale cartesian coords
    x = (x) * size
    y = (y) * size
    
    x+=size
    y+=size

    #adjust to center on screen
    #x += settings.WIDTH//2-size
    #y += settings.HEIGHT//2-size
    return (x, y)

def pixel_to_axial(point, size=10): #point = pygame.Vector2
    #invert scaling
    x = point.x - size
    y = point.y - size

    x = x / size
    y = y / size

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

