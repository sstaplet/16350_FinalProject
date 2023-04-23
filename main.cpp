#include "searcher_planner.hpp"
#include "zombie_planner.hpp"


namespace std { // define hash function for nodes
	template <> struct hash<std::pair<int, int>> {
		std::size_t operator()(const std::pair<int, int>& N) const noexcept {
			int x = N.first;
			int y = N.second;
			// Matthew Szudzik Elegant Pairing Function 
			// : provides unique mapping of a pair of ints to one int
			// works for a great hashing function
			return (x >= y ? x * x + x + y : x + y * y);
		}
	};
}


double** generate_map() {
  return NULL;
}



int main() {

  // initiate all variable (searcher, zombie, lost, obstacle locations etc.)

  pos zombie1 = std::make_pair(0, 0);
  pos zombie2 = std::make_pair(0, 0);
  std::list<pos> zombies = {zombie1, zombie2}; // list of zombie locations

  // std::list<pos> lost; // list of lost people locations
  pos lost_person = std::make_pair(0, 0);
  pos searcher = std::make_pair(0, 0);

  std::list<pos> searchers = {searcher};
  std::list<pos> losts = {lost_person};

  bool is_searching = false;
  double** map;
  int x_size;
  int y_size;

  std::unordered_map<pos, action> searchers_next_action; /* Stores searcher's next action*/
  std::unordered_map<pos, action> zombies_next_action; /* Stores zombie's next action*/
  std::unordered_map<pos, bool> searcher_is_searching; /* Stores searching state of each searcher*/

  for (pos searcher : searchers) {
    searchers_next_action[searcher] = {0, 0};
  }

  for (pos zombie : zombies) {
    zombies_next_action[zombie] = {0, 0};
  }

  for (pos searcher : searchers) {
    /* Every searcher starts "running away" */
    searcher_is_searching[searcher] = false;
  }

  while (1) {

    /* Conduct the respective tasks per searcher */
    for (pos searcher : searchers) {

      /* check if searcher is near lost person (check curr_state's heuristic value in map,
       if its <= 1.4 then it is adjacent to it) */
      if (map[searcher.first][searcher.second] <= 1.4f) {
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
          searchers_next_action[searcher] = searcher_planner(searcher, zombies, map, x_size, y_size, searcher_is_searching[searcher]);

        } else {
          /* Zombie moving randomly, searcher is searching */
          
          if (searcher_is_searching[searcher] == false) {
            /* Compute heuristic map here because we just switched from running away
               to searching */
            map = generate_map();
            searcher_is_searching[searcher] = true;
          }

          /* Get next actions according to scenario */
          zombies_next_action[zombie] = zombie_planner(); /* false (random movement) */
          searchers_next_action[searcher] = searcher_planner(searcher, zombies, map, x_size, y_size, searcher_is_searching[searcher]);
        }
      }
    }

    /* apply all actions */
    for (pos searcher : searchers) {
      searcher.first += searchers_next_action[searcher].first;
      searcher.second += searchers_next_action[searcher].second;
    }
    for (pos zombie : zombies) {
      zombie.first += zombies_next_action[zombie].first;
      zombie.second += zombies_next_action[zombie].second;
    }
    

    /* Display Map Animation */


  }


  return 0;

}


