#citizen.py

import pygame
import settings
import Hex
import Astar

class Citizen:
    """
Each citizen is represented as a circle of a specific countries color   
    """

    def __init__(self, color, position, home_city, job, size=5):
        self.color = color
        self.position = position
        self.home_city = home_city
        self.size = size
        self.age = 25
        self.occupation = job
        self.speed = 2.0
        #self.q = q #(q,r)
        #self.r = r
        self.path = []
        self.state = "to_work" #"to_work" / "working" / "to_city" / "idle"
        self.work_start_time = None
        self.work_duration = 3.0
        self.carrying = None

        self.current_tile = home_city
        self.goal_tile = None 
            
    def update(self):
        
        if self.state == "to_work":
            if not self.goal_tile:
                self.state = "idle"
                return
            self.move_toward(self.goal_tile)
            if self.is_at_tile(self.goal_tile):
                self.state = "working"
        
        elif self.state == "working":
            if self.work_start_time is None:
                self.work_start_time = pygame.time.get_ticks()
            elapsed = (pygame.time.get_ticks() - self.work_start_time) / 1000

            if elapsed >= self.work_duration:
                self.Work()
                self.work_start_time = None
                self.state = "to_city"

        elif self.state == "to_city":
            self.move_toward(self.home_city)
            if self.is_at_tile(self.home_city):
                self.goal_tile = None
                if self.carrying:
                    self.home_city.addResource(self.carrying)
                    print('release')
                self.state = "idle"

        if self.state == "idle":
            self.goal_tile = self.getGoal()
            if self.goal_tile:
                self.state = "to_work"
            else:
                self.state = "idle"

    def move_toward(self, tile):
        direction = pygame.Vector2(tile.pixelX, tile.pixelY) - pygame.Vector2(self.position)
        if direction.length_squared() > 1:
            self.position += direction.normalize() * self.speed
     
    def is_at_tile(self, tile):
        return (pygame.Vector2(tile.pixelX, tile.pixelY) - pygame.Vector2(self.position)).length() < 2

    def release_claim(self):
        if self.goal_tile and self in self.goal_tile.tile_type.claimed_by:
            self.goal_tile.tile_type.claimed_by.remove(self)

    def Work(self):
        #harvest tile
        self.release_claim()
        self.goal_tile.tile_type.harvest() 
        self.carrying = self.goal_tile.tile_type.name
    
    def getGoal(self):
        if self.occupation == "farmer": 
            valid_tiles = []

            for row in settings.HEX_MAP.tiles:
                for tile in row:
                    if (
                       tile.tile_type.name == 'wheat'
                       and tile.tile_type.amount > 0 
                       and len(tile.tile_type.claimed_by) < 1
                    ):
                        valid_tiles.append(tile)

            if not valid_tiles:
                return None

            #sort tiles by distance to current tile
            valid_tiles.sort(key=lambda t: Hex.axial_distance(self.current_tile, t))
            
            chosen_tile = valid_tiles[0]            
            chosen_tile.tile_type.claimed_by.add(self)
            return chosen_tile

        return None

    def Draw(self):   
        #Draw citizen
        pygame.draw.circle(settings.SCREEN, self.color, self.position, self.size)
        pygame.draw.circle(settings.SCREEN, (0,0,0), self.position, self.size, 1)
        #draw state bubble
        if settings.DEBUG:
            job = self.occupation.title() if self.occupation else "Citizen"
            label = f"{job}: {self.state.replace('_',' ').title()}"
            font = pygame.font.SysFont(None, 16)
            text_surf = font.render(label, True, (255,255,255))
            text_rect = text_surf.get_rect(center=(self.position.x, self.position.y - self.size -12))
            
            #background bubble
            bubble_padding = 4
            bubble_rect = text_rect.inflate(bubble_padding * 2, bubble_padding*2)
            pygame.draw.rect(settings.SCREEN, (0,0,0), bubble_rect, border_radius=6)
            settings.SCREEN.blit(text_surf, text_rect)
        

    def __repr__(self):
        return f"<Citizen at {self.position}, home={self.home_city.name}>"
