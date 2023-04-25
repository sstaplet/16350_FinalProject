import random

# create a randomly generated map
def createMap(fName, mode):
    f = open(fName, 'w')

    # different obstacle sizes and orientations
    obSzs = [2, 5, 7]
    choices = ['hor', 'vert', 'diag']
    dirs = [(1, 0), (0, 1), (1, 1)]

    # sets up parameters based on mode
    if mode == 0:
        numObs = 5
        numZs = 1
        mapSz = 30
    elif mode == 1:
        numObs = 20
        numZs = 2
        mapSz = 100
    else:
        numObs = 50
        numZs = 4
        mapSz = 1000

    # create base map
    map = []
    for i in range(mapSz):
        row = []
        for j in range(mapSz):
            row.append('0')
        map.append(row)

    # generates the number of obsstacles needed
    for i in range(numObs):
        # choose random size and orientation
        obSz = obSzs[random.randint(0,len(obSzs)-1)]
        orientation = random.choice(choices)

        # find top, left corner
        if (orientation == 'hor'):
            dir = 0
            left = random.randint(0, mapSz - obSz-1)
            top = random.randint(0, mapSz-1)
        elif (orientation == 'vert'):
            dir = 1
            top = random.randint(0, mapSz - obSz-1)
            left = random.randint(0, mapSz-1)
        else:
            dir = 2
            left = random.randint(0, mapSz - obSz-1)
            top = random.randint(0, mapSz - obSz-1)

        # create obstacle
        for j in range(obSz):
            (dx, dy) = dirs[dir]
            x = left + (j*dx)
            y = top + (j*dy)
            map[y][x] = '1'

    # place searcher
    while True:
        x = random.randint(0, mapSz -1)
        y = random.randint(0, mapSz -1)
        if (map[y][x] == '0'):
            map[y][x] = '2'
            break

    # place lost person
    while True:
        x = random.randint(0, mapSz -1)
        y = random.randint(0, mapSz -1)
        if (map[y][x] == '0'):
            map[y][x] = '3'
            break

    # place zombies
    for i in range(numZs):
        while True:
            x = random.randint(0, mapSz -1)
            y = random.randint(0, mapSz -1)
            if (map[y][x] == '0'):
                map[y][x] = '4'
                print(x,y)
                break

    # create the file
    for line in map:
        for char in line:
            f.write(char)
        f.write('\n')
