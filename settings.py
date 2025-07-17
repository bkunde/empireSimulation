#settings.py

import pygame
import random

DEBUG = False
FULL_SCREEN = (1280, 720)
WIDTH = int(FULL_SCREEN[0]/2)
HEIGHT = int(FULL_SCREEN[1]/2)
FRAME_RATE = 30
SCREEN = None
HEX_MAP = None


#HELPER FUNCTIONS
#--------------------------------#

#gets a random position on the screen
#returns a pygame Vector2
def randomPosition(): 
    xAxis = random.randint(0,WIDTH)
    yAxis = random.randint(0,HEIGHT)
    
    return pygame.Vector2(xAxis, yAxis)

#https://observablehq.com/@jrus/hexround
def axial_round(x, y):
    xgrid = round(x)
    ygrid = round(y)
    #store remainders
    x -= xgrid
    y -= ygrid
    
    if abs(x) >= abs(y):
        return (xgrid + round(x+0.5*y), ygrid)
    else:
        return (xgrid, ygrid + round(y+0.5*x))



def cube_round(frac_q, frac_r): #using axial coords 
    #q and r are passed in as fractions
    frac_s = -frac_q - frac_r#s = -q - r
    s = round(frac_s) 
    q = round(frac_q)
    r = round(frac_r)

    q_diff = abs(q - frac_q)
    r_diff = abs(r - frac_r)
    s_diff = abs(s - frac_s)
    
    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        s = -q-r
    
    return (q,r)
