from math import sqrt

NUMOFDIRS = 8

dXY = [(-1,-1), (-1, 0), (-1, 1), (0, -1), 
       (0, 1), (1, -1), (1, 0), (1, 1)]

def in_bounds(x: int, y: int, x_size: int, y_size: int) -> bool: 
    # might need to modify these bounds
    return ((x >= 1) and (y >= 1) and (x <= x_size) and (y <= y_size))

def euclid_dist(loc1: tuple, loc2: tuple) -> float:
    # gets the euclidean distance between two locations on the map
    print(loc1)
    print(loc2)
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(pow(dx, 2) + pow(dy, 2))

def in_view(person: tuple, entity: tuple, dist: int) -> bool:
    return (euclid_dist(person, entity) < dist)

def heuristic(loc1: tuple, loc2: tuple) -> float:
    # computes heuristic from lecture for LRTA
    x1 = loc1[0]
    y1 = loc1[1]
    x2 = loc2[0]
    y2 = loc2[1]

    return max(abs(x1 - x2), abs(y1 - y2)) + 0.4*min(abs(x1 - x2), abs(y1 - y2))

def generateMap(lost, x_size, y_size) -> list:
    # Generates a 2D list that emulates a map where each entry is the heuristic
    # value of that node with respect to the goal state
    map = []
    
    for row in range(0, y_size):

        temp_col = []
        for col in range(0, x_size):
            curr_pos = (row, col)
            temp_col.append(heuristic(curr_pos, lost))
            # temp_col = temp_col + []
        map.append(temp_col)
    
    # Print Map Row by Row
    # for j in range(0,y_size):
    #     print(map[j])
    return map

def getNearestEntityFromList(curr_state: tuple, entity_positions: list) -> tuple:
    # iterates though list of zombies and determines which is the closest
    closest_entity = (-1, -1)
    smallest_dist = -1

    for entity in entity_positions:
        
        curr_dist = euclid_dist(curr_state, entity)

        if (smallest_dist == -1):
            smallest_dist = curr_dist
            closest_entity = entity
        else:
            if (smallest_dist > curr_dist):
                smallest_dist = curr_dist
                closest_entity = entity


    return closest_entity

def getNearestEntityFromDict(curr_state: tuple, entity_pos: dict) -> tuple:
    closest_entity = (-1, -1)
    smallest_dist = -1

    for id in entity_pos:
        entity = entity_pos[id]
        print(entity)
        curr_dist = euclid_dist(curr_state, entity)

        if (smallest_dist == -1):
            smallest_dist = curr_dist
            closest_entity = entity
        else:
            if (smallest_dist > curr_dist):
                smallest_dist = curr_dist
                closest_entity = entity

    if (closest_entity == (-1, -1)):
        # all lost people found, go to arena exit
        return (0, 0)

    return closest_entity

def getRunawayAction(curr_state: tuple, nearest_zombie: tuple, map: list, x_size: int, y_size: int) -> tuple:
    # given the searcher's position and the position of the nearest zombie,
    # determine the action that greedily run's away and maximizes distance from
    # the zombie

    # Choose the action that maximizes the distance from the zombie, 
    # but minimizes the distance from the goal


    best_action = (0, 0)
    best_dist = -1

    for (dx, dy) in dXY:
        
        next_state = (curr_state[0] + dx, curr_state[1] + dy)
        if not in_bounds(next_state[0], next_state[1], x_size, y_size):
            continue

        curr_dist = euclid_dist(next_state, nearest_zombie)



        if (best_dist == -1):
            best_dist = curr_dist
            best_action = (dx, dy)

        else:
            if (best_dist < curr_dist):
                best_dist = curr_dist
                best_action = (dx, dy)


    return (best_action, map)

    

def LRTA(curr_state: tuple, map: list, x_size: int, y_size: int) -> tuple:
    
    # returns the next action and the state of the map once the action is
    # enacted

    next_action = (0, 0)

    best_neighbor = (0, 0)
    best_f = -1

    for (dx, dy) in dXY: 
        neighbor = (curr_state[0] + dx, curr_state[1] + dy)
        if not in_bounds(neighbor[0], neighbor[1], x_size, y_size):
            continue
        
        heuristic_val = map[neighbor[0]][neighbor[1]]

        if ((dx == 0) or (dy == 0)):
            graph_cost = 1
        else:
            graph_cost = 1.4

        f = heuristic_val + graph_cost

        if (best_f == -1):
            best_f = f
            best_neighbor = neighbor
        else:
            if (best_f > f):
                best_f = f
                best_neighbor = neighbor

    # print(best_neighbor)
    next_action = (best_neighbor[0] - curr_state[0], best_neighbor[1] - curr_state[1])
    
    if (best_f > map[curr_state[0]][curr_state[1]]):
        map[curr_state[0]][curr_state[1]] = best_f
    
    return (next_action, map) 


def searcherPlanner(curr_state: tuple, nearest_zombie: tuple, map: list, x_size: int, y_size: int, searching: bool) -> tuple:
    # returns the corresponding next action according to current state's searching state
    new_map = map
    if (searching):
        (next_action, new_map) = LRTA(curr_state, map, x_size, y_size)
    else:
        (next_action, new_map) = getRunawayAction(curr_state, nearest_zombie, map, x_size, y_size)
    
    return (next_action, new_map)


def planner():

    return







