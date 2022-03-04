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
  maze pdf FILENAME [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-S] [-L] [-O ORIENTATION] [-i MAZE_ID]
  maze text [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-L] [-i MAZE_ID]
  maze svg FILENAME [-W WIDTH] [-H HEIGHT] [-p PAGE_SIZE] [-d DENSITY] [-S] [-L] [-i MAZE_ID] [-s SOLUTION_FILENAME]

Options:
  -h, --help                        Show this help message and exit

  -W --width WIDTH                  Number of cells wide [default: 21]
  -H --height HEIGHT                Number of cells high [default: 30]

  -d --density DENSITY              Density of under/overs [default: 50]

  -L                                Enable a loop

  -S                                Draw with straight lines instead of curves

  -p PAGE_SIZE                      Page size, (A4 or Letter) [default: A4]
  -O --orientation ORIENTATION      Orientation, P=portrait, L=landscape [default: P]

  -i --maze_id MAZE_ID              Identify which maze, otherwise a random maze will be generated
  
  -s --solution SOLUTION_FILENAME   Save the solution to the maze to a file

Examples:

maze pdf my_new_maze.pdf

'''

import sys
import uuid
from random import randint, seed, shuffle

from docopt import docopt

try:
    from renderers.pdf import pdf_render
    from renderers.text import text_render
    from renderers.svg import svg_render
except ImportError:
    from maze.renderers.pdf import pdf_render  # NOQA
    from maze.renderers.text import text_render  # NOQA
    from maze.renderers.svg import svg_render  # NOQA

# constants to aid with describing the passage directions
N, S, E, W, U = 0x1, 0x2, 0x4, 0x8, 0x10
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {E: W, W: E, N: S, S: N}


class Tree(object):
    _children_for_parent = {}
    _parent_for_child = {}

    def __init__(self):
        Tree._children_for_parent[self] = set()
        Tree._parent_for_child[self] = self

    def connected(self, tree):
        return (Tree._parent_for_child[self] == Tree._parent_for_child[tree])

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
    sets = [[Tree() for x in range(width)] for y in range(height)]

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

            if (grid[cy][cx] != 0 or sets[ny][nx].connected(sets[sy][sx]) or sets[ey][ex].connected(sets[wy][wx])):
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
                    (x == cx and y == cy) or (x == ex and y == ey and d == W) or (x == sx and y == sy and d == N))]

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


def get_moves(grid, coordinate, cell):
    # for a given position, return all the posible coordinate moves
    moves = []

    y = coordinate[1]
    x = coordinate[0]
    if cell & W == W:
        inc = -1
        # if the next cell is an under or over cell, jump over it
        while grid[y][x + inc] in (19, 28):  # could be more than one in a row
            inc -= 1
        moves.append((inc, 0))
    if cell & E == E:
        inc = 1
        while grid[y][x + inc] in (19, 28):
            inc += 1
        moves.append((inc, 0))
    if cell & N == N:
        inc = -1
        while grid[y + inc][x] in (19, 28):
            inc -= 1
        moves.append((0, inc))
    if cell & S == S:
        inc = 1
        while grid[y + inc][x] in (19, 28):
            inc += 1
        moves.append((0, inc))
    return moves


def search(grid, coordinate, sofar, depth):
    cell = grid[coordinate[1]][coordinate[0]]

    for move in get_moves(grid, coordinate, cell):
        new_coordinate = (coordinate[0] + move[0], coordinate[1] + move[1])

        # if are back to where we where, then are in a loop
        if new_coordinate in sofar:
            continue

        new_so_far = [s for s in sofar]
        new_so_far.append(new_coordinate)

        # are we at the end already?
        if new_coordinate[0] == len(grid[0]) - 1 and new_coordinate[1] == len(grid) - 1:
            return new_so_far

        solution = search(grid, new_coordinate, new_so_far, depth + 1)
        if solution:
            return solution


def find_solution(grid):
    return search(grid, (0, 0), [(0, 0)], 0)


def maze(args):
    width = int(args['--width'])
    height = int(args['--height'])
    density = int(args['--density'])

    # allow the same maze to be generated if a maze_id is given.
    maze_id = args.get('--maze_id', None)
    if maze_id is None:
        maze_id = uuid.uuid4()
    seed(f"{maze_id}")

    filename = args['FILENAME']

    add_a_loop = args['-L']

    if args['-p'] not in ('A4', 'a4', 'Letter', 'letter'):
        print('Page size can only be A4 or Letter')
        print("e.g.  -p A4")
        print("You had -p", args['-p'])
        exit(-1)

    use_A4 = True if args['-p'] == 'A4' else False

    grid = create_maze(width, height, density, add_a_loop)

    solution = None
    solution_filename = args['--solution']
    if solution_filename:
        solution = find_solution(grid)

    # render options
    options = {'filename': filename, 'draw_with_curves': not args['-S'], 'use_A4': use_A4,
               'landscape': args['--orientation'] == 'L', 'width': width, 'height': height, 'solution': solution}

    if args['pdf']:
        pdf = pdf_render(grid, options)
        with open(filename, 'wb') as f:
            f.write(pdf)

    # to screen
    if args['text']:
        text_render(grid, options)

    if args['svg']:
        options['solution'] = []
        svg_with_solution = svg_render(grid, options)
        if solution_filename:
            options['solution'] = solution
            svg = svg_render(grid, options)
            with open(solution_filename, 'w') as f:
                f.write(svg)
        with open(filename, 'w') as f:
            f.write(svg_with_solution)


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print(__doc__)
        exit()

    maze(docopt(__doc__))
