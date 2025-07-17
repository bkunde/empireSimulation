#Debugger.py

import pygame
import settings
import Hex

hovered_tile = None

def TileInspector(hexGrid):
    global hovered_tile
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    if (pygame.mouse.get_pressed()[0]):
        frac_q, frac_r = Hex.pixel_to_axial(mouse_pos)
        q,r = settings.axial_round(frac_q, frac_r)
        
        for row in hexGrid.tiles:
            for tile in row:
                if tile.q == q and tile.r == r:
                    if hovered_tile != tile:
                        #revert previous tile
                        if hovered_tile:
                            hovered_tile.color = hovered_tile.get_color()
                        hovered_tile = tile
                        tile.color = (255,0,190)
                        print(tile)
                    break

    elif hovered_tile and not pygame.mouse.get_pressed()[0]:
        hovered_tile.color = hovered_tile.get_color()
        hovered_tile = None
    

    
