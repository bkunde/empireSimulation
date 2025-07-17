#ASTAR.py
import queue
import Hex
import settings


def astar(startHex, goal): 
    frontier = queue.PriorityQueue()
    frontier.put(startHex, 0) #the start hex, using q and r
    came_from = dict()
    cost_so_far = dict()
    came_from[startHex] = None
    cost_so_far[startHex] = 0

    while not frontier.empty():
        current = frontier.get()
    
        if current.terrain_type == goal:
           break
        for i in range(6): #six directions
            q,r =  Hex.hex_neighbor(current.q, current.r, i)
            nextHex = settings.HEX_MAP.tiles[q][r]
            new_cost = cost_so_far[current] + 1 # graph.cost(current, nextHex)
            if nextHex not in cost_so_far or new_cost < cost_so_far[nextHex]:
                cost_so_far[nextHex] = new_cost
                priority = new_cost + heuristic(goal, nextHex)
                frontier.put(nextHex, priority)
                came_from[nextHex] = current


def heuristic(goal, nextHex): #both are next tiles
    dist = Hex.axial_distance(goal, nextHex)
    #scale distance by diffiucltiy of terrain
    dist *= 1 #<--- DIFFICULTIY TO BE SET IN TILE
    print(dist)
    return dist
    
