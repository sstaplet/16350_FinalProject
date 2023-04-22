#include "lib.h"

action LRTA(pos start, pos goal, double** map, int x_size, int y_size) {

  action next_action;
  
  // get all neighbors
  // use each neighbor's heuristic and cost to move there to compute least expensive move among neighbors

  return std::make_pair(+1, +1);
}

pos get_nearest(pos curr_state, std::list<pos> zombie_positions) {
  /* iterates though list of zombies and determines which is the closest*/
}


action get_runaway_action(pos curr_state, pos nearest_zombie) {
  /* given the searcher's position and the position of the nearest zombie,
     determine the action that greedily run's away and maximizes distance from
     the zombie */
}


action searcher_planner(pos curr_state, pos goal, std::list<pos> zombie_positions, double** map, int x_size, int y_size, bool searching) {
  action next_action;

  // will be searching if searcher is not within zombie's visibility (proximity)
  if (searching) {
    /* In searching mode (LRTA*) */
    next_action = LRTA(curr_state, goal, map, x_size, y_size);
  } else {
    /* Running away from zombies (Greedy) */
    // look through the zombie list and run away from the nearest zombie
    pos nearest_zombie = get_nearest(curr_state, zombie_positions);
    next_action = get_runaway_action(curr_state, nearest_zombie);
  }
  
  curr_state.first += next_action.first;
  curr_state.second += next_action.second;

  return next_action;
}



pos get_nearest_lost() {}



