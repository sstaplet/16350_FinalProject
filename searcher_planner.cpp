#include "searcher_planner.h"

bool in_bounds(int x, int y, int x_size, int y_size) {
	return (x >= 1 && y >= 1 && x <= x_size && y <= y_size);
}

action LRTA(pos curr_state, double** map, int x_size, int y_size) {
  action next_action;
  
  
  pos best_neighbor = {-1, -1};
  double best_f = -1;

  // look through all neighbors for the nearest neighbor
  for (int dir = 0; dir< NUMOFDIRS; dir++) {

    /* Get an adjacent neighbor */
    pos neighbor = {curr_state.first + dX[dir], curr_state.second + dY[dir]};

    /* Check if neighbor is within bounds of map*/
    if (!in_bounds(curr_state.first, curr_state.second, x_size, y_size)) {
      continue;
    }

    /* Get neighbor's hueristic from the map */
    int heuristic_val = map[neighbor.first][neighbor.second];

    /* Get the cost to travel to this neighbor from the current state*/
    double graph_cost;
    if (dX[dir] == 0 || dY[dir] == 0) { // moving up/down/left/right
      graph_cost = (double)1;
    }
    else { // moving diagonally    
      graph_cost = 1.4;
    }

    /* Compute the f value */
    double f = heuristic_val + graph_cost;

    /* Get the neighbor who has the lowest f value */
    if (best_f == -1) {
      /* this is the first neighbor in the neighborhood*/
      best_f = f;
      best_neighbor = neighbor;
    } else {
      if (best_f > f) {
        best_f = f;
        best_neighbor = neighbor;
      }
    }
  }

  /* determine the action needed to move to the cheapest neighbor */
  action next_action = {best_neighbor.first - curr_state.first, best_neighbor.second - curr_state.second};

  /* Update the current state's heuristic value in the map*/
  map[curr_state.first][curr_state.second] = best_f;

  return next_action;
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
    next_action = LRTA(curr_state, map, x_size, y_size);
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


