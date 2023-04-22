#include "searcher_planner.hpp"
#include "zombie_planner.hpp"



int main() {

  // initiate all variable (searcher, zombie, lost, obstacle locations etc.)

  std::list<pos> zombies; // list of zombie locations
  pos zombie1 = std::make_pair(0, 0);
  pos zombie2 = std::make_pair(0, 0);
  zombies.push_back(zombie1);
  zombies.push_back(zombie2);

  // std::list<pos> lost; // list of lost people locations
  pos lost_person = std::make_pair(0, 0);
  pos searcher = std::make_pair(0, 0);

  bool is_searching = false;
  double** map;
  int x_size;
  int y_size;

  bool near_zombie;
  while (1) {
    
    /* check if searcher is near lost person (check curr_state's heuristic value in map,
       if its <= 1.4 then it is adjacent to it) */
    

    // check if searcher is within any zombie's viewing distance
    

    if (near_zombie) {
      is_searching = false;
    } else {
      is_searching = true;
    }  

    /* Determine which lost person is closest to the searcher */
    // pos lost_target = get_nearest_lost();

    /* Check if nearest lost person is within proximity */
    /*..................*/

    /* Determine everyone's next action */
    action searchers_next_action = searcher_planner(searcher, zombies, map, x_size, y_size, is_searching);
    // action zombie_next_action = zombie_planner();

    /* apply all actions */
    searcher.first += searchers_next_action.first;
    searcher.second += searchers_next_action.second;


    // zombie.first += zombie_next_action.first;
    // zombie.second += zombie_next_action.second;

    

    /* Display Map Animation */
  }




  return 0;
}


