#
# Ported to Python from https://gist.github.com/856138
#
#

# --------------------------------------------------------------------
# An implementation of a "weave" maze generator. Weave mazes are those
# with passages that pass both over and under other passages. The
# technique used in this program was described to me by Robin Houston,
# and works by first decorating the blank grid with the over/under
# crossings, and then using Kruskal's algorithm to fill out the rest
# of the grid. (Kruskal's is very well-suited to this approach, since
# it treats the cells as separate sets and joins them together.)
# --------------------------------------------------------------------
# NOTE: the display routine used in this script requires a terminal
# that supports ANSI escape sequences. Windows users, sorry. :(
# --------------------------------------------------------------------

from random import shuffle, seed, randint
from time import sleep
import sys
import argparse


def maze(width=10, height=10, density=50, _seed=None, delay=0.0):
    # delay, if bigger than 0, will display the intial maze, and step through

    # --------------------------------------------------------------------
    # 1. Allow the maze to be customized via command-line parameters
    # --------------------------------------------------------------------

    if _seed is None:
        _seed = randint(0, 90010000)
    seed(_seed)

    # --------------------------------------------------------------------
    # 2. Set up constants to aid with describing the passage directions
    # --------------------------------------------------------------------

    N, S, E, W, U = 0x1, 0x2, 0x4, 0x8, 0x10
    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W:  0, N: -1, S: 1}
    OPPOSITE = {E: W, W: E, N: S, S: N}

    # --------------------------------------------------------------------
    # 3. Data structures and methods to assist the algorithm
    # --------------------------------------------------------------------

    EW, NS, SE, SW, NE, NW = ["\xE2\x94%c" % v for v in
        [0x80, 0x82, 0x8C, 0x90, 0x94, 0x98]]
    NSE, NSW, EWS, EWN = ["\xE2\x94%c" % v for v in [0x9C, 0xA4, 0xAC, 0xB4]]

    TILES = {
      0: ["\x1B[47m   \x1B[m", "\x1B[47m   \x1B[m"],
      N: ["%s %s" % (NS, NS), "%s%s%s" % (NE, EW, NW)],
      S: ["%s%s%s" % (SE, EW, SW), "%s %s" % (NS, NS)],
      E: ["%s%s%s" % (SE, EW, EW), "%s%s%s" % (NE, EW, EW)],
      W: ["%s%s%s" % (EW, EW, SW), "%s%s%s" % (EW, EW, NW)],
      N | S: ["%s %s" % (NS, NS), "%s %s" % (NS, NS)],
      N | W: ["%s %s" % (NW, NS), "%s%s%s" % (EW, EW, NW)],
      N | E: ["%s %s" % (NS, NE), "%s%s%s" % (NE, EW, EW)],
      S | W: ["%s%s%s" % (EW, EW, SW), "%s %s" % (SW, NS)],
      S | E: ["%s%s%s" % (SE, EW, EW), "%s %s" % (NS, SE)],
      E | W: ["%s%s%s" % (EW, EW, EW), "%s%s%s" % (EW, EW, EW)],
      N | S | E: ["%s %s" % (NS, NE), "%s %s" % (NS, SE)],
      N | S | W: ["%s %s" % (NW, NS), "%s %s" % (SW, NS)],
      E | W | N: ["%s %s" % (NW, NE), "%s%s%s" % (EW, EW, EW)],
      E | W | S: ["%s%s%s" % (EW, EW, EW), "%s %s" % (SW, SE)],
      N | S | E | W: ["%s %s" % (NW, NE), "%s %s" % (SW, SE)],
      N | S | U: ["%s %s" % (NSW, NSE), "%s %s" % (NSW, NSE)],
      E | W | U: ["%s%s%s" % (EWN, EW, EWN), "%s%s%s" % (EWS, EW, EWS)]
    }

    def display_maze(grid):
        # top corner
        print "\x1B[H"
        print 'S'
        for z, row in enumerate(grid):
            # upper/lower rows
            for i in [0, 1]:
                for cell in row:
                    print TILES[cell][i],
                if z == len(grid[0]) - 1 and i == 1:
                    print 'E'
                else:
                    print
        print

    class Tree(object):

        def __init__(self):
            self.parent = None

        def root(self):
            if self.parent:
                return self.parent.root()
            return self

        def connected(self, tree):
            return(self.root() == tree.root())

        def connect(self, tree):
            tree.root().parent = self

    grid = [[0 for x in range(width)] for x in range(height)]
    sets = [[Tree() for x in range(width)] for x in range(height)]

    # build the list of edges
    edges = []
    for y in range(height):
        for x in range(width):
            if y > 0:
                edges.append([x, y, N])
            if x > 0:
                edges.append([x, y, W])

    shuffle(edges)

    # --------------------------------------------------------------------
    # 4. Build the over/under locations
    # --------------------------------------------------------------------

    print "\x1B[2J"  # clear the screen

    for cy in range(height - 2):
        cy += 1
        for cx in range(width - 2):
            cx += 1

            #next unless rand(100) < density
            if randint(0, 99) < density:
                continue

            nx, ny = cx, cy - 1
            wx, wy = cx - 1, cy
            ex, ey = cx + 1, cy
            sx, sy = cx, cy + 1

            if (grid[cy][cx] != 0 or
                sets[ny][nx].connected(sets[sy][sx]) or
                sets[ey][ex].connected(sets[wy][wx])):
                continue

            sets[ny][nx].connect(sets[sy][sx])
            sets[ey][ex].connect(sets[wy][wx])

            if randint(0, 1) == 0:
                grid[cy][cx] = E | W | U
            else:
                grid[cy][cx] = N | S | U

            grid[ny][nx] |= S
            grid[wy][wx] |= E
            grid[ey][ex] |= W
            grid[sy][sx] |= N

            edges[:] = [(x, y, d) for (x, y, d) in edges if not (
              (x == cx and y == cy) or
              (x == ex and y == ey and d == W) or
              (x == sx and y == sy and d == N)
            )]

            if delay:
                display_maze(grid)
                sleep(delay)

    if delay:
        print
        print "--- PRESS ENTER TO BEGIN ---"
        sys.stdin.read(1)

    print "\x1B[2J"  # clear the screen

    # --------------------------------------------------------------------
    # 5. Kruskal's algorithm
    # --------------------------------------------------------------------

    while edges:
        x, y, direction = edges.pop()
        nx, ny = x + DX[direction], y + DY[direction]

        set1, set2 = sets[y][x], sets[ny][nx]

        if not set1.connected(set2):
            if delay:
                display_maze(grid)
                sleep(delay)

            set1.connect(set2)
            grid[y][x] |= direction
            grid[ny][nx] |= OPPOSITE[direction]

    display_maze(grid)

    # --------------------------------------------------------------------
    # 6. Show the parameters used to build this maze, for repeatability
    # --------------------------------------------------------------------

    print "width=%d, height=%d, density=%d, seed=%d" % (width,
                                            height, density, _seed)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate a maze')

    parser.add_argument('-W', dest="width", type=int,
        help='width (default=10)', default=10)
    parser.add_argument('-H', dest="height", type=int,
        help='height (default=10)', default=10)
    parser.add_argument('-D', dest="density", type=int,
        help='density (default=50)', default=50)

    parser.add_argument('-d', dest="delay", type=float,
        help="delay in seconds. (default=0), e.g. -d 0.01",
        default=0.0)

    args = parser.parse_args()

    # do it
    maze(**vars(args))

#
