#!/usr/bin/env python
'''

Maze.

An implementation of a "weave" maze generator. Weave mazes are those
with passages that pass both over and under other passages. The
technique used in this program was described by Robin Houston,
and works by first decorating the blank grid with the over/under
crossings, and then using Kruskal's algorithm to fill out the rest
of the grid. (Kruskal's is very well-suited to this approach, since
it treats the cells as separate sets and joins them together.)

Please note: this program was oringally ported from
https://gist.github.com/856138

Usage:
  maze -h
  maze pdf FILENAME [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-S] [-L] [-O ORIENTATION]
  maze text [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-L]
  maze canvas [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-L] [-f FILENAME]
  maze javascript [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-L] [-f FILENAME]
  maze svg [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-L] [-f FILENAME]
  maze data [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-S] [-L]

Options:
  -h, --help                    Show this help message and exit

  -W --width WIDTH              Number of cells wide [default: 21]
  -H --height HEIGHT            Number of cells high [default: 30]

  -d --density DENSITY          Density of under/overs [default: 50]

  -L                            Enable a loop

  -S                            Draw with straight lines instead of curves

  -p PAGE_SIZE                  Page size, (A4 or Letter) [default: A4]
  -O --orientation ORIENTATION  Orientation, P=portrait, L=landscape [default: P]


Examples:

maze pdf my_new_maze.pdf


'''

from random import shuffle, randint, seed
import sys
from docopt import docopt

# constants to aid with describing the passage directions
N, S, E, W, U = 0x1, 0x2, 0x4, 0x8, 0x10
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W:  0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}

#


class Tree(object):

    _children_for_parent = {}
    _parent_for_child = {}

    def __init__(self):

        Tree._children_for_parent[self] = set()
        Tree._parent_for_child[self] = self

    def connected(self, tree):
        return (Tree._parent_for_child[self] ==
                Tree._parent_for_child[tree])

    def connect(self, tree):

        # find root objs
        new_parent = Tree._parent_for_child[self]
        tree_patent = Tree._parent_for_child[tree]

        # move parent
        Tree._children_for_parent[new_parent].add(tree_patent)

        # move children
        children = Tree._children_for_parent[tree_patent]
        Tree._children_for_parent[new_parent] |= children
        Tree._children_for_parent[tree_patent] = set()

        # move parent for child keys too
        for child in Tree._children_for_parent[new_parent]:
            Tree._parent_for_child[child] = new_parent


def create_maze(width, height, density, add_a_loop):

    # structures to hold the maze
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

    # build the over/under locations
    for cy in range(height - 2):
        cy += 1
        for cx in range(width - 2):
            cx += 1

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

    # Kruskal's algorithm
    while edges:
        x, y, direction = edges.pop()
        nx, ny = x + DX[direction], y + DY[direction]

        set1, set2 = sets[y][x], sets[ny][nx]

        if not set1.connected(set2):
            set1.connect(set2)
            grid[y][x] |= direction
            grid[ny][nx] |= OPPOSITE[direction]

    # add in a loop, I just replace a under/over with a cross
    if add_a_loop:
        # find all the crossing, if any
        candiates = []
        for cy in range(height - 2):
            cy += 1
            for cx in range(width - 2):
                cx += 1
                if grid[cy][cx] in (U | N | S, U | E | W):
                    candiates.append((cy, cx))

        # change just one of them to a crossing, e.g. create a loop
        if len(candiates):
            shuffle(candiates)
            cy, cx = candiates[0]
            grid[cy][cx] = N | S | W | E

    return grid


def maze(args):

    width = int(args['--width'])
    height = int(args['--height'])
    density = int(args['--density'])

    filename = args['FILENAME']

    add_a_loop = args['-L']

    if args['-p'] not in ('A4', 'a4', 'Letter', 'letter'):
        print('Page size can only be A4 or Letter')
        print("e.g.  -p A4")
        print("You had -p", args['-p'])
        exit(-1)

    use_A4 = True if args['-p'] == 'A4' else False

    dislay_to_screen = args['text']
    generate_canvas_js = args['canvas']
    generate_js = args['javascript']
    generate_svg = args['svg']
    generate_data = args['data']
    generate_pdf = args['pdf']

    if generate_data:
        filename = "maze.pdf"

    # render options
    render_options = {'filename': filename,
                      'draw_with_curves': not args['-S'],
                      'use_A4': use_A4,
                      'landscape': args['--orientation'] == 'L',
                      'width': width,
                      'height': height}

    grid = create_maze(width, height, density, add_a_loop)

    return_data = {}
    # to pdf, if we have a filename
    if filename and generate_data or generate_pdf:

        try:
            from renderers.pdf import render
        except ImportError:
            from maze.renderers.pdf import render  # NOQA

        return_data['pdf'] = render(grid, render_options)

    # to screen
    if dislay_to_screen:
        try:
            from renderers.text import render
        except ImportError:
            from maze.renderers.text import render  # NOQA

        render(grid, render_options)

    if generate_canvas_js:
        try:
            from renderers.canvas import render
        except ImportError:
            from maze.renderers.canvas import render  # NOQA

        return_data['canvas'] = render(grid, render_options)
        if filename and not generate_data:
            with open(filename, 'w') as f:
                f.write(return_data['canvas'])

    if generate_js or generate_data:
        try:
            from renderers.js import render
        except ImportError:
            from maze.renderers.js import render  # NOQA

        return_data['js'] = render(grid, render_options)
        if filename and not generate_data:
            with open(filename, 'w') as f:
                f.write(return_data['js'])

    if generate_svg or generate_data:
        try:
            from renderers.svg import render
        except ImportError:
            from maze.renderers.svg import render  # NOQA

        return_data['svg'] = render(grid, render_options)
        if filename and not generate_data:
            with open(filename, 'w') as f:
                f.write(return_data['svg'])

    return return_data


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print(__doc__)
        exit()

    maze(docopt(__doc__))

#
