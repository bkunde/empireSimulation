#Debugger.py

import pygame
import settings
import Hex

hovered_tile = None
has_printed = False

def TileInspector(hexGrid):
    global hovered_tile, has_printed
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    if (pygame.mouse.get_pressed()[0]):
        frac_q, frac_r = Hex.pixel_to_axial(mouse_pos)
        q,r = settings.axial_round(frac_q, frac_r)
        
        for row in hexGrid.tiles:
            for tile in row:
                if tile.q == q and tile.r == r:
                    if hovered_tile != tile:
                        if hovered_tile:
                            hovered_tile.highlighted = False

                        hovered_tile = tile
                        hovered_tile.highlighted = True
                        print(tile)
                    """
                        #revert previous tile
                            hovered_tile.color = hovered_tile.get_color()
                        hovered_tile = tile
                        tile.color = (255,0,190)
                        """
                    break

    elif hovered_tile: #and not (settings.SCREEN.get_rect().collidepoint(pygame.mouse.get_pos())): #(pygame.mouse.get_pressed()[0]):
        hovered_tile.highlighted = False
        hovered_tile = None
    

    
