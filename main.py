#Brevin Kunde 7/1/25

import pygame
import random
import settings, Debugger
import Citizen, Empire, Hex, City, Resource, Map

def Main():
    pygame.init()
    settings.SCREEN = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    #create citizens, will probably be moved to its own file
    #for i in range(5):
        #country.createCitizens()

    settings.HEX_MAP = Hex.HexMap(size=10)
    #print(settings.HEX_MAP)
    
    empire = Empire.Empire(color=(240,233,27))
    #create a start city
    city = City.City(12, 12, 'city', empire)
    settings.HEX_MAP.tiles[city.q][city.r].setTile(city)

    #print(settings.HEX_MAP.tiles[x].q, settings.HEX_MAP.tiles[x].r)

    mapcreator = Map.Map()
    seed=random.randint(0,10000)
    mapcreator.generateMap(seed=seed)

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                running = False #quit the game
            if keys[pygame.K_b]:
                settings.DEBUG = not(settings.DEBUG) #toggle debug mode 

            if keys[pygame.K_UP]:
                seed += random.randint(2, 1000)
                mapcreator.generateMap(seed)
            if keys[pygame.K_DOWN]:
                seed -= random.randint(2, 1000)
                mapcreator.generateMap(seed)
        
        #RENDER SIMULATION
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
    
