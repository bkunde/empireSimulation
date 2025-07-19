#Brevin Kunde 7/1/25

import pygame
import random, time
import settings, Debugger
import Citizen, Empire, Hex, City, Resource, Map

def Main():
    pygame.init()
    settings.SCREEN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    lastMapUpdate = 0
    cooldown = 0.3
	
    settings.HEX_MAP = Hex.HexMap(size=10)
    
    #print(settings.HEX_MAP.tiles[x].q, settings.HEX_MAP.tiles[x].r)

    #create and draw map
    mapcreator = Map.Map()
    seed=random.randint(0,10000)
    mapcreator.generateMap(seed=seed)
    prevSeed = seed

    #create a start city
    empire = Empire.Empire(color=(255,0,0))
    city = City.City(20, 11, 'city', empire)
    hex_tile = settings.HEX_MAP.getTile(city.q, city.r)
    if hex_tile:
        hex_tile.setTile(city)
        

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False #quit the game
            if keys[pygame.K_b]:
                settings.DEBUG = not(settings.DEBUG) #toggle debug mode 

            now = time.time()
            if keys[pygame.K_RIGHT] and now - lastMapUpdate > cooldown:
                prevSeed = seed
                seed += random.randint(2, 1000)
                mapcreator.generateMap(seed)
                if hex_tile:
                    hex_tile.setTile(city)
                lastMapUpdate = now
            if keys[pygame.K_LEFT] and now - lastMapUpdate > cooldown:
                seed = prevSeed
                mapcreator.generateMap(seed)
                if hex_tile:
                    hex_tile.setTile(city)
                lastMapUpdate = now
        
        ###RENDER SIMULATION###
        #Update Phase
        for citizen in city.citizens:
            citizen.update()

        city.update()
        mapcreator.update()

        #Draw Phase
        settings.SCREEN.fill("black")
        settings.HEX_MAP.draw()
        
        #for citizen in country.citizens:
        for citizen in city.citizens:
            citizen.Draw()
        
        ###DEBUG###
        if settings.DEBUG:
            Debugger.TileInspector(settings.HEX_MAP)

        #flip screen to display
        pygame.display.flip()
    
        #make any movment frame rate independent
        dt = clock.tick(settings.FRAME_RATE) / 1000

    pygame.quit()
    return 0 

if __name__  == '__main__':
    Main()
    
