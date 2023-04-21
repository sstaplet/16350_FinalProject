/*=================================================================
 *
 * lostplanner.c
 *
 *=================================================================*/
#include <math.h>
#include <iostream>
#include <queue>
#include <cstdlib>
#include <algorithm>
#include <vector>
using namespace std;

/* Input Arguments */
#define	MAP_IN      prhs[0]
#define	ROBOT_IN	prhs[1]
#define	GOAL_IN     prhs[2]


/* Output Arguments */
#define	ACTION_OUT	plhs[0]

//access to the map is shifted to account for 0-based indexing in the map, whereas
//1-based indexing in matlab (so, robotpose and goalpose are 1-indexed)
#define GETMAPINDEX(X, Y, XSIZE, YSIZE) ((Y-1)*XSIZE + (X-1))

#if !defined(MAX)
#define	MAX(A, B)	((A) > (B) ? (A) : (B))
#endif

#if !defined(MIN)
#define	MIN(A, B)	((A) < (B) ? (A) : (B))
#endif

#define NUMOFDIRS 8



int lost = 3;
int temp = 0;

//node class for priority queue
struct Node {
    int x;
    int y;
    double h;
    Node(){
        this->x = 0;
        this->y = 0;
        this->h = 0.0;
    }
    Node(const int x, const int y, double h)
        : x(x), y(y), h(h)
    {
    }
    void updateh(double h){
        this->h = h;
    }
};

//comparison function for priority queue
class compareCost{
    public:
    bool operator()(Node n1, Node n2)
    {
        //mexPrintf("f1: %f, f2: %f\n", n1.f, n2.f);
        return n1.h > n2.h;
    }
};

double findDist(int i, int j, int curX, int curY){
    return sqrt(pow(double(i - curX),2) + pow(double(j - curY),2));
}

//go through the map and find the nearest lost person
int* findNearestLostPerson(double* map, int xDim, int yDim, int curX, int curY){
    //set up dist, x, y to be changed later
    double dist = xDim*yDim;
    int x = -1;
    int y = -1;
    //go through each x dimension
    for(int i = 0; i < xDim; i++){
        //go through each y dimension
        for(int j = 0; j < yDim; j++){
            //get the map index and check if it's a lost person
            int mIndex = GETMAPINDEX(i, j, xDim, yDim);
            if (map[mIndex] == lost){
                //find the distance from the lost person to you and adjust if closer
                double thisDist = findDist(i, j, curX, curY);
                if (thisDist < dist){
                    dist = thisDist;
                    x = i;
                    y = j;
                }
            }
        }
    }
    //return final location found
    int location[2] = {x, y};
    return location;
}

//create a graph of nodes including heuristics
Node** createGraph(double*	map, int xDim, int yDim, int curX, int curY){
    int* lostPos = findNearestLostPerson(map, xDim, yDim, curX, curY);
    //create the node list in the 'vertical dimension' and start to fill in
    Node** g = (Node**) malloc(yDim*sizeof(Node*));
    for (int i = 0; i < yDim; i++){
        //create the node list in the 'horizontal dimension' and add in Nodes
        Node* row = (Node*) malloc(xDim*sizeof(Node));
        for(int j = 0; j < xDim; j++){
            row[j] = Node(i, j, findDist(i, j, lostPos[0], lostPos[1]));
        }
        g[i] = row;
    }
    return g;
}

main(){
return 0;}
