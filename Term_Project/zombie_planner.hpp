#ifndef ZOMBIE_PLAN
#define ZOMBIE_PLAN
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

#define NUMOFDIRS 8


typedef std::pair<int, int> pos;
typedef std::pair<int, int> action;


action zombie_planner() {
  return std::make_pair(0, 0);
}



#endif /* ZOMBIE_PLAN */