#pragma once
#include <unordered_map>
#include <utility>
#include <queue>
#include <iostream> 

#define GETMAPINDEX(x, y, xsize, ysize) ((y-1)*xsize + (x-1))

#if !defined(MAX)
#define	MAX(a, b)	((a) > (b) ? (a) : (b))
#endif

#if !defined(MIN)
#define	MIN(a, b)	((a) < (b) ? (a) : (b))
#endif

typedef std::pair<int, int> pos;
typedef std::pair<int, int> action;

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


void zombie_planner() {}

void main() {

  // initiate all variable (searcher, zombie, lost, obstacle locations etc.)

  // std::list<pos> zombies; // list of zombie locations
  pos zombie = std::make_pair(0, 0);
  // std::list<pos> lost; // list of lost people locations
  pos lost_person = std::make_pair(0, 0);
  pos searcher = std::make_pair(0, 0);

  bool is_searching = false;

  while (1) {

    // check if searcher is within any zombie's viewing distance
    
    if (/*searcher is within proximity of zombie*/) {
      is_searching = false;
    } else {
      is_searching = true;
    }  

    /* Determine which lost person is closest to the searcher */
    pos lost_target = get_nearest_lost();

    /* Check if nearest lost person is within proximity */
    /*..................*/

    /* Determine everyone's next action */
    action searchers_next_action = searcher_planner();
    action zombie_next_action = zombie_planner();

    /* apply all actions */
    searcher.first += searchers_next_action.first;
    searcher.second += searchers_next_action.second;

    zombie.first += zombie_next_action.first;
    zombie.second += zombie_next_action.second;

    

    /* Display Map Animation */
  }





}


