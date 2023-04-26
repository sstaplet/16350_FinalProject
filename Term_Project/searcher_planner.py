from math import sqrt


dXY = [(-1,-1), (-1, 0), (-1, 1), (0, -1), 
       (0, 1), (1, -1), (1, 0), (1, 1)]


def in_bounds(x: int, y: int, x_size: int, y_size: int) -> bool: 
    # might need to modify these bounds
    return ((x >= 0) and (y >= 0) and (x <= x_size - 1) and (y <= y_size - 1))


def euclid_dist(loc1: tuple, loc2: tuple) -> float:
    # gets the euclidean distance between two locations on the map
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
    
    return map


def getNearestEntityIDFromDict(curr_state: tuple, entity_pos: dict, lost_being_searched: list) -> int:
    # closest_entity = (0, 0)
    smallest_dist = -1
    closest_entity_ID = -1

    # There are no enitities in the dict
    if entity_pos == {}:
        return -1
        # return default_goal

    for id in entity_pos:
        entity = entity_pos[id]
        curr_dist = euclid_dist(curr_state, entity)

        if lost_being_searched != []: # We are looking at a dict of lost
            if id in lost_being_searched: 
                # Here we avoid returning a lost person that is already being tracked
                continue

        if (smallest_dist == -1):
            smallest_dist = curr_dist
            # closest_entity = entity
            closest_entity_ID = id
        else:
            if (smallest_dist > curr_dist):
                smallest_dist = curr_dist
                # closest_entity = entity
                closest_entity_ID = id

    return closest_entity_ID


def LRTA_OR_RUN(curr_state: tuple, zombie: tuple, map: list, x_size: int, y_size: int) -> tuple:
    # does same thing as LRTA, however, it avoids being adjacent to zombies
    next_action = (0, 0)

    best_neighbor = curr_state
    best_f = -1

    for (dx, dy) in dXY: 
        neighbor = (curr_state[0] + dx, curr_state[1] + dy)
        
        if not in_bounds(neighbor[0], neighbor[1], x_size, y_size):
            continue

        if (euclid_dist(neighbor, zombie) < 2):
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

    next_action = (best_neighbor[0] - curr_state[0], best_neighbor[1] - curr_state[1])
    
    if (best_f > map[curr_state[0]][curr_state[1]]):
        map[curr_state[0]][curr_state[1]] = best_f
    
    return (next_action, map)






