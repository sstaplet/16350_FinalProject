# import the pygame module, so you can use it
from planner import *

# Initialize Main Screen
logo = pygame.image.load("freddy.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Apocalypse Simulator")
background = pygame.transform.scale(pygame.image.load("grass.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
screen.blit(background, (0, 0))
drawGrid(map)


# Initialize entity structures
searcher_dict = dict()
lost_dict = dict()
zombie_dict = dict()

# Gives each entity a unique ID
id = 0 

# Fill in the entity structures
for i in range(len(ZSTARTX)):
    x = ZSTARTX[i]
    y = ZSTARTY[i]
    zombie_dict[id] = (x, y)
    id += 1

for i in range(len(LSTARTX)):
    x = LSTARTX[i]
    y = LSTARTY[i]
    lost_dict[id] = (x, y)
    id += 1

for i in range(len(SSTARTX)):
    x = SSTARTX[i]
    y = SSTARTY[i]
    searcher_dict[id] = (x, y)
    id += 1


def main():

    clockobject = pygame.time.Clock()

                        ###### Initialize Variables ######

    # Init images
    zombie_image = pygame.transform.scale(pygame.image.load("zombie.png"), (BLOCK_SIZE,BLOCK_SIZE))
    searcher_image = pygame.transform.scale(pygame.image.load("steve.png"), (BLOCK_SIZE,BLOCK_SIZE))
    lost_image = pygame.transform.scale(pygame.image.load("villager.png"), (BLOCK_SIZE,BLOCK_SIZE))
    goal_image = pygame.transform.scale(pygame.image.load("gold.png"), (BLOCK_SIZE,BLOCK_SIZE))

    # draw entities
    for id in zombie_dict:
        loc = zombie_dict[id]
        drawEntity(zombie_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), RED)

    for id in searcher_dict:
        loc = searcher_dict[id]
        drawEntity(searcher_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), BLUE)

    for id in lost_dict:
        loc = lost_dict[id]
        drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), GREEN)

    
    pygame.display.update()


    # Defining algorithm vars.
    zombies_next_action = dict()
    searchers_map = dict()
    searchers_target = dict()
    being_searched = []

    # Initialize Seearcher Structures and Variables
    for searcher_ID in searcher_dict:
        nearest_lost_person_ID = getNearestEntityIDFromDict(searcher_dict[searcher_ID], lost_dict, [])
        nearest_lost_person = lost_dict[nearest_lost_person_ID]
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
        drawGrid(map)
        drawEntity(goal_image, getImageLoc(ARENA_EXIT), getOffsetLoc(getImageLoc(ARENA_EXIT), (0,0)), WHITE)
        # Main Algorithm

        # Compute all default zombie moves
        for zombie_ID in zombie_dict:
            if (tick % 2 == 0):
                zombies_next_action[zombie_ID] = zombie_planner(zombie_dict[zombie_ID], searcher_dict, map)
            else:
                zombies_next_action[zombie_ID] = (0, 0)

        tick += 1

        # # Conduct the respective tasks per searcher
        searcher_ID_list = list(searcher_dict.keys())
        # for searcher_ID in searcher_ID_list:
        n = 0
        while n < len(searcher_ID_list):

            searcher_ID = searcher_ID_list[n]
            searcher = searcher_dict[searcher_ID]
            curr_Hmap = searchers_map[searcher_ID]

            if (curr_Hmap[searcher[0]][searcher[1]] <= 1.5):
                for lost_ID in lost_dict:

                    lost = lost_dict[lost_ID]

                    if in_view(searcher, lost, 5):

                        # Move lost from lost dict to searcher dict
                        del lost_dict[lost_ID] # remove from lost dict
                        searcher_dict[lost_ID] = lost # add to searcher dict
                        searcher_ID_list.append(lost_ID)
                        # Generate new searchers new goal
                        nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_dict, being_searched)
                        being_searched.append(nearest_lost_person_ID) # This lost person is now being tracked, record it in being_searched
                        
                        if (nearest_lost_person_ID == -1): # If no lost left
                            goal = ARENA_EXIT
                        else:
                            goal = lost_dict[nearest_lost_person_ID]
                            
                        searchers_target[lost_ID] = nearest_lost_person_ID
                        searchers_map[lost_ID] = generateMap(goal, X_SIZE, Y_SIZE)

                        # Iterate through all searchers, to redirect any searcher
                        # who had been looking for this lost person
                        for searcher_ID in searcher_dict:
                            if searchers_target[searcher_ID] == lost_ID:
                                # Generate old searchers new goal
                                nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_dict, being_searched)
                                being_searched.append(nearest_lost_person_ID)# This lost person is now being tracked, record it in being_searched
                                
                                if (nearest_lost_person_ID == -1): # If no lost left
                                    goal = ARENA_EXIT
                                else:
                                    goal = lost_dict[nearest_lost_person_ID]
                                
                                searchers_target[searcher_ID] = nearest_lost_person_ID
                                searchers_map[searcher_ID] = generateMap(goal, X_SIZE, Y_SIZE)
                                
                        curr_Hmap = searchers_map[searcher_ID] # Update current searchers map

                        break # break here because we have already found out lost person
            
            # Find the nearest zombie
            nearest_zombie_ID = getNearestEntityIDFromDict(searcher, zombie_dict, [])
            nearest_zombie = zombie_dict[nearest_zombie_ID]

            (searcher_next_action, new_map) = LRTA(searcher, nearest_zombie, curr_Hmap, map, X_SIZE, Y_SIZE)
            # Update the searchers map if it changes (due to LRTA)
            
            searchers_map[searcher_ID] = new_map

            # Apply next actions

            searcher = (searcher[0] + searcher_next_action[0], searcher[1] + searcher_next_action[1])
            searcher_dict[searcher_ID] = searcher
            drawEntity(searcher_image, getImageLoc(searcher), getOffsetLoc(getImageLoc(searcher), (0,0)), BLUE)


            # Check if searcher has reached goal
            remove_from_searchers_list = []
            for searcher_ID in searcher_dict:
                searcher_loc = searcher_dict[searcher_ID]
                if (euclid_dist(searcher_loc, ARENA_EXIT) < 1):
                    print("A searcher has exited the arena!!!")
                    remove_from_searchers_list.append(searcher_ID)

            # Check if zombie has caught any searcher:
            for searcher_ID in searcher_dict:
                searcher_loc = searcher_dict[searcher_ID]
                for zombie_ID in zombie_dict:
                    zombie_loc = zombie_dict[zombie_ID]
                    if (zombie_loc == searcher_loc):
                        # Remove searcher if they're eaten
                        remove_from_searchers_list.append(searcher_ID)
                        searcher_ID_list.remove(searcher_ID)
                        n -= 1
                        print("MISSION FAILED: ZOMBIE HAS EATEN A CIVILLIAN!")
                        break

            # Delete searchers if they have reached the goal
            for elem in remove_from_searchers_list:
                del searcher_dict[elem]

            # Once all searchers are gone (escaped or dead)
            if searcher_dict == {}:
                print("Simulation Complete")
                running = False
                break

            # End of Loop
            n += 1
            

        ###################### ANIMATION UPDATE HERE ###########################

        for loc_ID in lost_dict:
            # Apply action
            loc = lost_dict[loc_ID]
            # Plot new position
            drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), GREEN)

        for zombie_ID in zombie_dict:
            # Apply action
            zombie_loc = zombie_dict[zombie_ID]
            (dx, dy) = zombies_next_action[zombie_ID]
            zombie_dict[zombie_ID] = (zombie_loc[0] + dx, zombie_loc[1] + dy)
            # Plot new position
            drawEntity(zombie_image, getImageLoc(zombie_dict[zombie_ID]), getOffsetLoc(getImageLoc(zombie_dict[zombie_ID]), (0,0)), RED)

        
        # Event to check for closing tab
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                
        pygame.display.update()




# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__== "__main__":
    # call the main function
    main()