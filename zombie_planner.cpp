#ifndef ZOMBIE_PLAN
#define ZOMBIE_PLAN
#include <unordered_map>
#include <random>
#include <utility>
#include <queue>
#include <iostream> 
#include <cmath>
#include <math.h>

#define GETMAPINDEX(x, y, xsize, ysize) ((y-1)*xsize + (x-1))

#if !defined(MAX)
#define	MAX(a, b)	((a) > (b) ? (a) : (b))
#endif

#if !defined(MIN)
#define	MIN(a, b)	((a) < (b) ? (a) : (b))
#endif

#define NUMOFDIRS 8

using namespace std;


typedef std::pair<int, int> pos;
typedef std::pair<int, int> action;

srand(time(NULL));

int isSeen(pos curr_state, pos searcher, int radius) {
    int dist_x = pow(fabs(curr_state.first - searcher.first), 2);
    int dist_y = pow(fabs(curr_state.second - searcher.second), 2);
    int dist = sqrt(dist_x + dist_y);
    if (dist < radius) {
        return 1;
    } else {
        return 0;
    }
}

action zombie_planner(pos curr_state, pos searcher, int radius, double** map, int x_size, int y_size) {
    action next_action;

    int dirs[3] = {-1, 0, 1};

    int chase = isSeen(curr_state, searcher, radius);

    if (chase) {
        while(1) {
            int dx = dirs[rand()%3];
            int dy = dirs[rand()%3];

            int x = curr_state.first + dx;
            int y = curr_state.second + dy;

            if ((x <= x_size) || (y <= y_size)) {
                next_action.first = dx;
                next_action.second = dy;
                break;
            }
        }
    } else {
        int dx = curr_state.first - searcher.first;
        int dy = curr_state.second - searcher.second;

        double angle = atan2(dy, dx) * 180 / M_PI;

        if (angle < -157.5) {
            next_action.first = -1;
            next_action.second = 0;
        }
        else if (angle < -112.5) {
            next_action.first = -1;
            next_action.second = -1;
        }
        else if (angle < -67.5) {
            next_action.first = 0;
            next_action.second = -1;
        }
        else if (angle < -22.5) {
            next_action.first = 1;
            next_action.second = -1;
        }
        else if (angle <22.5) {
            next_action.first = 1;
            next_action.second = 0;
        } 
        else if (angle < 67.5) {
            next_action.first = 1;
            next_action.second = 1;
        }
        else if (angle < 112.5) {
            next_action.first = 0;
            next_action.second = 1;
        }
        else if (angle < 157.5) {
            next_action.first = -1;
            next_action.second = 1;
        } else {
            next_action.first = -1;
            next_action.second = 0;
        }
    }

    return next_action
    // return std::make_pair(0, 0);
}



#endif /* ZOMBIE_PLAN */