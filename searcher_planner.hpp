#ifndef SEARCH_PLAN
#define SEARCH_PLAN

#include <unordered_map>
#include <utility>
#include <queue>
#include <iostream> 
#include <list>
#include <math.h>

#define GETMAPINDEX(x, y, xsize, ysize) ((y-1)*xsize + (x-1))

#if !defined(MAX)
#define	MAX(a, b)	((a) > (b) ? (a) : (b))
#endif

#if !defined(MIN)
#define	MIN(a, b)	((a) < (b) ? (a) : (b))
#endif

#define NUMOFDIRS 8

int dX[NUMOFDIRS] = { -1, -1, -1,  0,  0,  1, 1, 1 };
int dY[NUMOFDIRS] = { -1,  0,  1, -1,  1, -1, 0, 1 };

typedef std::pair<int, int> pos;
typedef std::pair<int, int> action;

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
  next_action = {best_neighbor.first - curr_state.first, best_neighbor.second - curr_state.second};

  /* Update the current state's heuristic value in the map*/
  map[curr_state.first][curr_state.second] = best_f;

  return next_action;
}

double euclid_dist(pos loc1, pos loc2) {
  double dx = loc1.first - loc2.first;
  double dy = loc1.second - loc2.second;
  return sqrt(powf(dx, 2) + powf(dy, 2));
}

pos get_nearest(pos curr_state, std::list<pos> zombie_positions) {
  /* iterates though list of zombies and determines which is the closest*/
  
  pos closest_zombie;
  double smallest_dist = -1;

  for (pos zombie : zombie_positions) {

    double curr_dist = euclid_dist(curr_state, zombie);

    /* If this is the first zombie, by default its the closest one*/
    if (smallest_dist == -1) {
      smallest_dist = curr_dist;
      closest_zombie = zombie;
    } 
    else {
      /* Otherwise, if this zombie has a closer distance than the current closest,
         then update the closest zombie to be this one */
      if (smallest_dist > curr_dist) {
        smallest_dist = curr_dist;
        closest_zombie = zombie;
      }
    }
  }

  return closest_zombie;
}


action get_runaway_action(pos curr_state, pos nearest_zombie) {
  /* given the searcher's position and the position of the nearest zombie,
     determine the action that greedily run's away and maximizes distance from
     the zombie */
  action best_action = {0, 0};
  double farthest_dist = -1;

  for (int dir = 0; dir < NUMOFDIRS; dir++) {

    pos next_state = {curr_state.first + dX[dir], 
                      curr_state.second + dY[dir]};

    double curr_dist = euclid_dist(next_state, nearest_zombie);

    if (farthest_dist == -1) {
      farthest_dist = curr_dist;
      best_action = {dX[dir], dY[dir]};
    } else {
      if (farthest_dist < curr_dist) {
        farthest_dist = curr_dist;
        best_action = {dX[dir], dY[dir]};
      }
    }
  }
  return best_action;
}


action searcher_planner(pos curr_state, std::list<pos> zombie_positions, double** map, int x_size, int y_size, bool searching) {
  
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



pos get_nearest_lost() {

  return std::make_pair(0,0);
}





#endif /* SEARCH_PLAN */
