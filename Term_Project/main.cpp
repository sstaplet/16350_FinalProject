#include "searcher_planner.hpp"
#include "zombie_planner.hpp"
#include "mex.h"


#define MAP_IN prhs[0]
#define ROBOT_IN prhs[1]


#define ACTION_OUT plhs[0]


static void planner() {

  // initiate all variable (map size, searcher, zombie, lost, obstacle locations etc.)
  int x_size;
  int y_size;

  /* TODO: Randomize/specify starting locations for lost, searchers, zombies */
  
  pos zombie1 = std::make_pair(0, 0);
  pos zombie2 = std::make_pair(0, 0);
 
  pos lost_person = std::make_pair(0, 0);
  pos searcher = std::make_pair(0, 0);


  std::unordered_map<pos, action> searchers_next_action; /* Stores searcher's next action*/
  std::unordered_map<pos, action> zombies_next_action; /* Stores zombie's next action*/
  std::unordered_map<pos, bool> searcher_is_searching; /* Stores searching state of each searcher*/
  std::unordered_map<pos, double**> searchers_map; /* Assigns each searcher a heuristic map */


  std::list<pos> searchers = {searcher}; /* List of all searcher locations */
  std::list<pos> losts = {lost_person}; /* List of all lost person locations */
  std::list<pos> zombies = {zombie1, zombie2}; /* List of zombie locations */

  for (pos searcher : searchers) {
    /* Every searcher's first move is null (+0, +0) */
    searchers_next_action[searcher] = {0, 0};

    /* Every searcher starts in a searching state */
    searcher_is_searching[searcher] = true;

    /* Assign heuristic maps accordingly */
    searchers_map[searcher] = generate_map();
  }

  for (pos zombie : zombies) {
    zombies_next_action[zombie] = {0, 0};
  }


  /* TODO: What if two searchers are assigned the same lost? Either need to terminate 
     the other's search when the lost is found, or only assign one lost to a searcher at
     a time */

  int n = 1;
  int N = 2000;
  while (n < N) { /* Run for N time-steps*/

    /* Conduct the respective tasks per searcher */
    for (pos searcher : searchers) {
      double** curr_map = searchers_map[searcher];

      /* check if searcher is near lost person (check curr_state's heuristic value in map,
       if its <= 1.4 then it is adjacent to it) */
      if (curr_map[searcher.first][searcher.second] <= 1.4f) {
        /* Find out which lost person is nearby */
        for (auto lost = losts.begin(); lost != losts.end(); ++lost) {
          /* Using an iterator type for "lost" here so that I can delete it from
             the losts list later (need to use * to derefernce "lost" to get "pos" type) */
          if (in_view(searcher, *lost, 5)) {
            /* Convert lost to searcher **might have to give it its own map** */
            losts.erase(lost);
            searchers.push_back(*lost);
            searcher_is_searching[*lost] = false;
            break; /* no need to continue iterating since we found our "lost" */
          }
        }
      }

      /* Conduct respective tasks per zombie for each searcher */
      for (pos zombie : zombies) {
        /* Check if zombie is within 5 Euclid Dist of this searcher */
        
        if (in_view(searcher, zombie, 5)) {
          /* Zombie chasing searcher, searcher running away */
          searcher_is_searching[searcher] = false;

          /* Get next actions according to scenario */
          zombies_next_action[zombie] = zombie_planner(); /* true (non-random, greedy movement) */
          searchers_next_action[searcher] = searcher_planner(searcher, zombies, curr_map, x_size, y_size, searcher_is_searching[searcher]);

        } else {
          /* Zombie moving randomly, searcher is searching */

          if (searcher_is_searching[searcher] == false) {
            /* Compute heuristic map here because we just switched from running away
               to searching */
            curr_map = generate_map();
            searcher_is_searching[searcher] = true;
          }

          /* Get next actions according to scenario */
          zombies_next_action[zombie] = zombie_planner(); /* false (random movement) */
          searchers_next_action[searcher] = searcher_planner(searcher, zombies, curr_map, x_size, y_size, searcher_is_searching[searcher]);
        }
      }
    }


    // OUTPUT ACTIONS

    // /* apply all actions */
    // for (pos searcher : searchers) {
    //   searcher.first += searchers_next_action[searcher].first;
    //   searcher.second += searchers_next_action[searcher].second;
    // }
    // for (pos zombie : zombies) {
    //   zombie.first += zombies_next_action[zombie].first;
    //   zombie.second += zombies_next_action[zombie].second;
    // }
    

    /* Display Map Animation */




    n++;
  }

}


void mexFunction(int nlhs, mxArray* plhs[], 
int nrhs, const mxArray* prhs[]) {

    



}















