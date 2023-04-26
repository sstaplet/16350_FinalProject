# import the pygame module, so you can use it
import pygame
import time
from random import randint
from searcher_planner import *


def drawEntity(image, entity_loc, image_loc, color):
    # screen.blit(image, image_loc)
    pygame.draw.circle(screen, color, entity_loc, 5, 0)
        

def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, (0,0,0), rect, 1)

def displayMap(map):
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            i = int(x/BLOCK_SIZE)
            j = int(y/BLOCK_SIZE)
            text_surface = my_font.render(str(int(map[i][j])), False, (0,0,120))
            screen.blit(text_surface, (x, y))

# COLORS
BLUE = (0,0,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Map (WINDOW/BLOCK_SIZE x WINDOW/BLOCK_SIZE) = (30x30 GRID)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

X_SIZE = int(WINDOW_WIDTH/BLOCK_SIZE)
Y_SIZE = int(WINDOW_HEIGHT/BLOCK_SIZE)



# Searcher Vars
SSTARTX = 28
SSTARTY = 28
SEARCHER_MAP_LOC = (SSTARTX, SSTARTY)
SEARCHER_OFFSET = (-95, -90) # for image centering purposes only
SEARCHER_START = (SSTARTX*BLOCK_SIZE, SSTARTY*BLOCK_SIZE)

# Lost Vars
LSTARTX = 12
LSTARTY = 12
LOST_MAP_LOC = (LSTARTX, LSTARTY)
LOST_OFFSET = (-15, -30) # for image centering purposes only
LOST_START = (LSTARTX*BLOCK_SIZE, LSTARTY*BLOCK_SIZE)


# Zombie Vars
ZSTARTX = 8
ZSTARTY = 9
ZOMBIE_MAP_LOC = (ZSTARTX, ZSTARTY)
ZOMBIE_OFFSET = (-42, -50) # for image centering purposes only
ZOMBIE_START = (ZSTARTX*BLOCK_SIZE, ZSTARTY*BLOCK_SIZE)

# Possible movement variations for Zombies
ZOMBIE_MOVEMENT_ADVANCED = [(-1,-1), (-1, 0), (-1, 1), (0, -1), 
                    (0, 1), (1, -1), (1, 0), (1, 1)]

ZOMBIE_MOVEMENT_NORMAL = [(+1, 0), (0, +1), (-1, 0), (0, -1)]

ZOMBIE_MOVEMENT = ZOMBIE_MOVEMENT_NORMAL


def zombie_planner(zombie_loc: tuple, searcher_pos: dict) -> tuple:
    # Returns the action that will minimize the distance between the zombie and
    # its closest searcher
    nearest_searcher_ID = getNearestEntityIDFromDict(zombie_loc, searcher_pos, [])
    nearest_searcher = searcher_pos[nearest_searcher_ID]
    smallest_dist = 1000
    best_action = (0, 0)

    for (dx, dy) in ZOMBIE_MOVEMENT:
        next_state = (zombie_loc[0] + dx, zombie_loc[1] + dy)

        curr_dist = euclid_dist(nearest_searcher, next_state)

        if (curr_dist < smallest_dist):
            smallest_dist = curr_dist
            best_action = (dx, dy)
    
    return best_action

def getOffsetLoc(loc, offset):
    # Gets images offset needed to center it on point
    return (loc[0] + offset[0], loc[1] + offset[1])

def getImageLoc(loc): 
    # Gets the images location on window with respect to the entries location
    # in the map list
    return (loc[0]*BLOCK_SIZE, loc[1]*BLOCK_SIZE)

def applyAction(loc, action):
    # Enacts and action on a location and returns new state
    return (loc[0] + action[0], loc[1] + action[1])

# initialize the pygame module
pygame.init()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MC', 16)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
logo = pygame.image.load("freddy.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Apocalypse Simulator")
background = pygame.transform.scale(pygame.image.load("grass.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
screen.blit(background, (0, 0))
drawGrid()

def main():

    clockobject = pygame.time.Clock()

    ###### Initialize Variables

    """
    We're using ID's in this implementation to keep track of each entity's 
    location in a concise manner.

    """

    # init zombie
    zombie_image = pygame.image.load("freddy.png")
    drawEntity(zombie_image, ZOMBIE_START, getOffsetLoc(ZOMBIE_START, ZOMBIE_OFFSET), RED)
    zombie_ID = 3
    zombie_pos = dict()
    zombie_pos[zombie_ID] = ZOMBIE_MAP_LOC

    zombie1_ID = 90
    zombie_pos[zombie1_ID] = (ZOMBIE_MAP_LOC[0] + 10, ZOMBIE_MAP_LOC[1] + 10)

    # init searcher
    searcher_image = pygame.image.load("Kobato.png")
    drawEntity(searcher_image, SEARCHER_START, getOffsetLoc(SEARCHER_START, SEARCHER_OFFSET), BLUE)
    searcher_ID = 1
    searcher_pos = dict()
    searcher_pos[searcher_ID] = SEARCHER_MAP_LOC
    

    # init lost
    lost_image = pygame.image.load("Isaac.png")
    drawEntity(lost_image, LOST_START, getOffsetLoc(LOST_START, LOST_OFFSET), GREEN)
    lost_ID = 2
    lost_pos = dict()
    lost_pos[lost_ID] = LOST_MAP_LOC

    lost2_ID = 4
    lost_pos[lost2_ID] = (LOST_MAP_LOC[0] + 10, LOST_MAP_LOC[1])

    lost2_ID = 5
    lost_pos[lost2_ID] = (LOST_MAP_LOC[0], LOST_MAP_LOC[1] + 5)

    lost2_ID = 6
    lost_pos[lost2_ID] = (LOST_MAP_LOC[0] - 5, LOST_MAP_LOC[1] + 15)
    

    ######

    pygame.display.update()

    ARENA_EXIT = (1,1)
    

    # Defining algorithm vars.

    zombies_next_action = dict()
    searchers_map = dict()
    searchers_target = dict()
    being_searched = []

    for searcher_ID in searcher_pos:
        nearest_lost_person_ID = getNearestEntityIDFromDict(searcher_pos[searcher_ID], lost_pos, [])
        nearest_lost_person = lost_pos[nearest_lost_person_ID]
        searchers_target[searcher_ID] = nearest_lost_person_ID # Map searcher ID to their target Lost person ID
        searchers_map[searcher_ID] = generateMap(nearest_lost_person, X_SIZE, Y_SIZE)
        being_searched.append(nearest_lost_person_ID) # Keep track of which lost are being searched to avoid aliasing

    # define a variable to control the main loop
    running = True
     
    # main loop
    tick = 0
    while running:
        clockobject.tick(5) # Set Frame rate to 10 fps

        # Refresh Screen
        screen.blit(background, (0,0))
        drawGrid()
        drawEntity(searcher_image, getImageLoc(ARENA_EXIT), getOffsetLoc(getImageLoc(ARENA_EXIT), SEARCHER_OFFSET), WHITE)
        
        # Main Algorithm

        # Compute all default zombie moves
        for zombie_ID in zombie_pos:
            if (tick % 2 == 0):
                zombies_next_action[zombie_ID] = zombie_planner(zombie_pos[zombie_ID], searcher_pos)
            else:
                zombies_next_action[zombie_ID] = (0, 0)

        tick += 1

        # # Conduct the respective tasks per searcher
        searcher_ID_list = list(searcher_pos.keys())
        # for searcher_ID in searcher_ID_list:
        n = 0
        while n < len(searcher_ID_list):

            searcher_ID = searcher_ID_list[n]
            searcher = searcher_pos[searcher_ID]
            curr_map = searchers_map[searcher_ID]

            if (curr_map[searcher[0]][searcher[1]] <= 1.5):
                for lost_ID in lost_pos:
                    lost = lost_pos[lost_ID]

                    if in_view(searcher, lost, 5):

                        # Move lost from lost dict to searcher dict
                        del lost_pos[lost_ID] # remove from lost dict
                        searcher_pos[lost_ID] = lost # add to searcher dict
                        searcher_ID_list.append(lost_ID)
                        # Generate new searchers new goal
                        nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_pos, being_searched)
                        being_searched.append(nearest_lost_person_ID) # This lost person is now being tracked, record it in being_searched
                        
                        if (nearest_lost_person_ID == -1): # If no lost left
                            goal = ARENA_EXIT
                        else:
                            goal = lost_pos[nearest_lost_person_ID]
                            
                        searchers_target[lost_ID] = nearest_lost_person_ID
                        searchers_map[lost_ID] = generateMap(goal, X_SIZE, Y_SIZE)

                        # Iterate through all searchers, to redirect any searcher
                        # who had been looking for this lost person
                        for searcher_ID in searcher_pos:
                            if searchers_target[searcher_ID] == lost_ID:
                                # Generate old searchers new goal
                                nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_pos, being_searched)
                                being_searched.append(nearest_lost_person_ID)# This lost person is now being tracked, record it in being_searched
                                
                                if (nearest_lost_person_ID == -1): # If no lost left
                                    goal = ARENA_EXIT
                                else:
                                    goal = lost_pos[nearest_lost_person_ID]
                                
                                searchers_target[searcher_ID] = nearest_lost_person_ID
                                searchers_map[searcher_ID] = generateMap(goal, X_SIZE, Y_SIZE)
                                
                                # curr_map = searchers_map[searcher_ID] # UPDATE current map 

                        curr_map = searchers_map[searcher_ID] # Update current searchers map

                        break # break here because we have already found out lost person
            
            # Find the nearest zombie
            nearest_zombie_ID = getNearestEntityIDFromDict(searcher, zombie_pos, [])
            nearest_zombie = zombie_pos[nearest_zombie_ID]

            (searcher_next_action, new_map) = LRTA_OR_RUN(searcher, nearest_zombie, curr_map, X_SIZE, Y_SIZE)
            # Update the searchers map if it changes (due to LRTA)
            
            searchers_map[searcher_ID] = new_map

            # Apply next actions

            searcher = (searcher[0] + searcher_next_action[0], searcher[1] + searcher_next_action[1])
            searcher_pos[searcher_ID] = searcher
            drawEntity(searcher_image, getImageLoc(searcher), getOffsetLoc(getImageLoc(searcher), SEARCHER_OFFSET), BLUE)


            # Check if zombie has caught any searcher:
            for searcher_ID in searcher_pos:
                searcher_loc = searcher_pos[searcher_ID]
                for zombie_ID in zombie_pos:
                    zombie_loc = zombie_pos[zombie_ID]
                    if (zombie_loc == searcher_loc):
                        print("MISSION FAILED: ZOMBIE HAS EATEN A CIVILLIAN!")

            # Check if searcher has reached goal
            remove_from_searchers_list = []
            for searcher_ID in searcher_pos:
                searcher_loc = searcher_pos[searcher_ID]
                if (euclid_dist(searcher_loc, ARENA_EXIT) < 1):
                    print("A searcher has exited the arena!!!")
                    remove_from_searchers_list.append(searcher_ID)

            # Delete searchers if they have reached the goal
            for elem in remove_from_searchers_list:
                del searcher_pos[elem]

            if searcher_pos == {}:
                print("Simulation Complete")
                running = False
                break

            # End of Loop
            n += 1
            

        ###################### ANIMATION UPDATE HERE ###########################

        for loc_ID in lost_pos:
            # Apply action
            loc = lost_pos[loc_ID]
            # Plot new position
            drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), LOST_OFFSET), GREEN)

        for zombie_ID in zombie_pos:
            # Apply action
            zombie_loc = zombie_pos[zombie_ID]
            (dx, dy) = zombies_next_action[zombie_ID]
            zombie_pos[zombie_ID] = (zombie_loc[0] + dx, zombie_loc[1] + dy)
            # Plot new position
            drawEntity(zombie_image, getImageLoc(zombie_pos[zombie_ID]), getOffsetLoc(getImageLoc(zombie_pos[zombie_ID]), ZOMBIE_OFFSET), RED)


        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                
        pygame.display.update()




# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()