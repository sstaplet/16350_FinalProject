her_is_searching[searcher_ID] == False):
                    # Check if searcher just swapped from 
                    nearest_lost_person = getNearestEntityFromDict(searcher, lost_pos)
                    # generate a map with respect to the nearest lost person
                    curr_map = generateMap(nearest_lost_person, X_SIZE, Y_SIZE)
                    searcher_is_searching[searcher_ID] = True