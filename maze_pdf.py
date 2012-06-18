# -*- coding: utf-8 -*-
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
import argparse
from reportlab.pdfgen.canvas import Canvas


def maze(width=10, height=10, density=50, _seed=None):

    _seed = 1
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

    def display_maze(grid):

        c = Canvas('xx.pdf')
        c.setTitle('Maze')
        c.setSubject("")
        c.setAuthor("Dale O'Brien")

        page_width = 8.5 * 72
        page_height = 11.0 * 72

        c.setPageSize((page_width, page_height))

        # 0=butt,1=round,2=square
        c.setLineCap(1)

        left_margin = 10
        top_margin = 10

        cell_size = (page_width - 2 * left_margin) / width
        gap = 4
        c.setLineWidth(gap)

        for j, row in enumerate(grid):
            # upper/lower rows
            for i, cell in enumerate(row):

                x_offset = left_margin + i * cell_size
                y_offset = top_margin + j * cell_size

                c.translate(x_offset, y_offset)
                p = c.beginPath()

                if cell == 1:
                    # TODO: add arcs ...

                    '│ │'
                    '└─┘'

                    p.moveTo(gap, 0)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, 0)

                    #p.arcTo(gap, cell_size / 2.0,
                    #         cell_size - gap, cell_size - gap,
                    #        0, 180)

                if cell == 2:

                    '┌─┐'
                    '│ │'

                    p.moveTo(gap, cell_size)
                    p.lineTo(gap, gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, cell_size)

                if cell == 3:

                    '│ │'
                    '│ │'

                    p.moveTo(gap, cell_size)
                    p.lineTo(gap, 0)
                    p.moveTo(cell_size - gap, cell_size)
                    p.lineTo(cell_size - gap, 0)

                if cell == 4:

                    '┌──'
                    '└──'

                    p.moveTo(cell_size, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(gap, gap)
                    p.lineTo(cell_size, gap)

                if cell == 5:

                    '│ └'
                    '└──'

                    p.moveTo(gap, 0)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(cell_size, cell_size - gap)

                    p.moveTo(cell_size,  gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, 0)

                if cell == 6:

                    '┌──'
                    '│ ┌'

                    p.moveTo(cell_size,  cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size)

                    p.moveTo(cell_size, gap)
                    p.lineTo(gap, gap)
                    p.lineTo(gap, cell_size)

                if cell == 7:

                    '│ └'
                    '│ ┌'

                    p.moveTo(gap, cell_size)
                    p.lineTo(gap, 0)

                    p.moveTo(cell_size, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size)

                    p.moveTo(cell_size,  gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, 0)

                if cell == 8:

                    '──┐'
                    '──┘'

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(0, gap)

                if cell == 9:

                    '┘ │'
                    '──┘'

                    p.moveTo(0, gap)
                    p.lineTo(gap, gap)
                    p.lineTo(gap, 0)

                    p.moveTo(cell_size - gap, 0)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(0, cell_size - gap)

                if cell == 10:

                    '──┐'
                    '┐ │'

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(gap, cell_size)

                    p.moveTo(0, gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, cell_size)

                if cell == 11:

                    '┘ │'
                    '┐ │'

                    p.moveTo(cell_size - gap, cell_size)
                    p.lineTo(cell_size - gap, 0)

                    p.moveTo(0, gap)
                    p.lineTo(gap, gap)
                    p.lineTo(gap, 0)

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(gap, cell_size)

                if cell == 12:

                    '───'
                    '───'

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(cell_size, cell_size - gap)
                    p.moveTo(0, gap)
                    p.lineTo(cell_size, gap)

                if cell == 13:

                    '┘ └'
                    '───'

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(cell_size, cell_size - gap)

                    p.moveTo(0, gap)
                    p.lineTo(gap, gap)
                    p.lineTo(gap, 0)

                    p.moveTo(cell_size,  gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, 0)
                if cell == 14:

                    '───'
                    '┐ ┌'

                    p.moveTo(0, gap)
                    p.lineTo(cell_size, gap)

                    p.moveTo(cell_size, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size)

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(gap, cell_size)

                if cell == 15:

                    '┘ └'
                    '┐ ┌'

                    p.moveTo(0, gap)
                    p.lineTo(gap, gap)
                    p.lineTo(gap, 0)

                    p.moveTo(cell_size, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size)

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)
                    p.lineTo(gap, cell_size)

                    p.moveTo(cell_size,  gap)
                    p.lineTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, 0)

                if cell == 19:

                    '┤ ├'
                    '┤ ├'

                    p.moveTo(gap, cell_size)
                    p.lineTo(gap, 0)
                    p.moveTo(cell_size - gap, cell_size)
                    p.lineTo(cell_size - gap, 0)

                    p.moveTo(0, gap)
                    p.lineTo(gap, gap)
                    p.moveTo(0, cell_size - gap)
                    p.lineTo(gap, cell_size - gap)

                    p.moveTo(cell_size, gap)
                    p.lineTo(cell_size - gap, gap)
                    p.moveTo(cell_size, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size - gap)

                if cell == 28:

                    '┴─┴'
                    '┬─┬'

                    p.moveTo(0, cell_size - gap)
                    p.lineTo(cell_size, cell_size - gap)
                    p.moveTo(0, gap)
                    p.lineTo(cell_size, gap)

                    p.moveTo(gap, gap)
                    p.lineTo(gap, 0)
                    p.moveTo(gap, cell_size - gap)
                    p.lineTo(gap, cell_size)

                    p.moveTo(cell_size - gap, gap)
                    p.lineTo(cell_size - gap, 0)
                    p.moveTo(cell_size - gap, cell_size - gap)
                    p.lineTo(cell_size - gap, cell_size)

                c.drawPath(p)
                c.translate(-x_offset, -y_offset)

        c.save()

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

    for cy in range(height - 2):
        for cx in range(width - 2):

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

    # --------------------------------------------------------------------
    # 5. Kruskal's algorithm
    # --------------------------------------------------------------------

    while edges:
        x, y, direction = edges.pop()
        nx, ny = x + DX[direction], y + DY[direction]

        set1, set2 = sets[y][x], sets[ny][nx]

        if not set1.connected(set2):

            set1.connect(set2)
            grid[y][x] |= direction
            grid[ny][nx] |= OPPOSITE[direction]

    display_maze(grid)

    # --------------------------------------------------------------------
    # 6. Show the parameters used to build this maze, for repeatability
    # --------------------------------------------------------------------

    #print "width=%d, height=%d, density=%d, seed=%d" % (width,
    #                                        height, density, _seed)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate a maze')

    parser.add_argument('-W', dest="width", type=int,
        help='width (default=10)', default=20)
    parser.add_argument('-H', dest="height", type=int,
        help='height (default=10)', default=20)
    parser.add_argument('-D', dest="density", type=int,
        help='density (default=50)', default=50)

    args = parser.parse_args()

    # do it
    maze(**vars(args))

#
