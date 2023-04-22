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


action searcher_planner(pos curr_state, 
pos goal, std::list<pos> zombie_positions, 
double** map, int x_size, int y_size, bool searching);

action LRTA(pos start, pos goal, double** map, int x_size, int y_size);

pos get_nearest(pos curr_state, std::list<pos> zombie_positions);

action get_runaway_action(pos curr_state, pos nearest_zombie);

pos get_nearest_lost();


