# import the pygame module, so you can use it
import pygame
import time
from random import randint
from searcher_planner import *

f = open("test.txt", 'r')
map = f.readlines()
f.close()

mapSz = len(map)

BLOCK_SIZE = 600//mapSz
WINDOW_WIDTH = BLOCK_SIZE * mapSz
WINDOW_HEIGHT = BLOCK_SIZE * mapSz

BLUE = (0,0,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Searcher Vars
SSTARTX = 20
SSTARTY = 15
# SEARCHER_OFFSET = (-95, -90)
# SEARCHER_START = (SSTARTX*BLOCK_SIZE, SSTARTY*BLOCK_SIZE)

# Lost Vars
LSTARTX = 5
LSTARTY = 2
# LOST_OFFSET = (-15, -30)
# LOST_START = (LSTARTX*BLOCK_SIZE, LSTARTY*BLOCK_SIZE)

# Zombie Vars
ZSTARTX = []
ZSTARTY = []
# ZOMBIE_OFFSET = (-42, -50)
# ZOMBIE_START = (ZSTARTX*BLOCK_SIZE, ZSTARTY*BLOCK_SIZE)
def drawEntity(image, entity_loc, image_loc, color):
    screen.blit(image, image_loc)
    pygame.draw.circle(screen, color, entity_loc, 5, 0)
def drawGrid(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            val = m[i][j]
            if val == '0':
                c = BLACK
                s = 1
            elif val == '1':
                c = BLACK
                s = 0
            elif val == '2':
                c = BLUE
                s = 1
                global SSTARTX
                SSTARTX = j
                global SSTARTY
                SSTARTY = i
                print(j, i)
            elif val == '3':
                c = WHITE
                s = 1
                global LSTARTX
                LSTARTX = j
                global LSTARTY
                LSTARTY = i
            elif val == '4':
                c = RED
                s = 1
                global ZSTARTX
                ZSTARTX.append(j)
                global ZSTARTY
                ZSTARTY.append(i)
            x = j * BLOCK_SIZE
            y = i * BLOCK_SIZE
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, c, rect, s)

def getImageLoc(loc, offset):
    return (loc[0] + offset[0], loc[1] + offset[1])

def applyAction(loc, action):
    return (loc[0] + action[0], loc[1] + action[1])


# initialize the pygame module
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
logo = pygame.image.load("freddy.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Apocalypse Simulator")
background = pygame.transform.scale(pygame.image.load("grass.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
screen.blit(background, (0, 0))
drawGrid(map)

SEARCHER_OFFSET = (-95, -90)
#print(SSTARTX,SSTARTY)
SEARCHER_START = (SSTARTX*BLOCK_SIZE, SSTARTY*BLOCK_SIZE)

LOST_OFFSET = (-15, -30)
LOST_START = (LSTARTX*BLOCK_SIZE, LSTARTY*BLOCK_SIZE)

ZOMBIE_OFFSET = (-42, -50)
ZOMBIE_START = []
for i in range(len(ZSTARTX)):
    x = ZSTARTX[i]*BLOCK_SIZE
    y = ZSTARTY[i]*BLOCK_SIZE
    ZOMBIE_START.append((x,y))

def main():

    clockobject = pygame.time.Clock()

    ###### Initialize Variables

    #init zombie
    zombie = pygame.transform.scale(pygame.image.load("freddy.png"), (BLOCK_SIZE,BLOCK_SIZE))
    for loc in ZOMBIE_START:
        drawEntity(zombie, loc, getImageLoc(loc, (0,0)), RED)

    zombie_list = ZOMBIE_START + []

    # init searcher
    searcher = pygame.transform.scale(pygame.image.load("Kobato.png"), (BLOCK_SIZE,BLOCK_SIZE))
    drawEntity(searcher, SEARCHER_START, getImageLoc(SEARCHER_START, (0,0)), BLUE)

    searcher_list = [SEARCHER_START]


    # init lost
    lost = pygame.transform.scale(pygame.image.load("Isaac.png"), (BLOCK_SIZE,BLOCK_SIZE))
    drawEntity(lost, LOST_START, getImageLoc(LOST_START, (0,0)), GREEN)

    lost_list = [LOST_START]

    #init map
    #map = generateMap()

    ######

    pygame.display.update()


    # define a variable to control the main loop
    running = True

    # main loop
    time = 0
    while running:
        # clockobject.tick(5) # Set Frame rate to 10 fps
        #
        # searcher_next_action = (randint(-1, 1)*BLOCK_SIZE,
        #                         randint(-1, 1)*BLOCK_SIZE)
        #
        # # Refresh Screen
        # screen.blit(background, (0,0))
        # drawGrid()
        #
        # # Apply actions and update locations
        #
        # for loc in searcher_list:
        #     # Apply action
        #     loc = applyAction(loc, searcher_next_action)
        #     # Plot new position
        #     drawEntity(searcher, loc, getImageLoc(loc, SEARCHER_OFFSET), BLUE)
        #
        # for loc in lost_list:
        #     # Apply action
        #     loc = loc
        #     # Plot new position
        #     drawEntity(lost, loc, getImageLoc(loc, LOST_OFFSET), GREEN)
        #
        # for loc in zombie_list:
        #     # Apply action
        #     loc = loc
        #     # Plot new position
        #     drawEntity(zombie, loc, getImageLoc(loc, ZOMBIE_OFFSET), RED)
        #
        #
        # # event handling, gets all event from the event queue
        # for event in pygame.event.get():
        #     # only do something if the event is of type QUIT
        #     if event.type == pygame.QUIT:
        #         # change the value to False, to exit the main loop
        #         running = False

        pygame.display.update()




# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()