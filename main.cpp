#include "searcher_planner.h"
#include "zombie_planner.h"

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


