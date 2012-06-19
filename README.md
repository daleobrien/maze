maze
====

Maze generator with crossing;

    python maze_pdf.py    

will produce a pdf, much like this one by default;

https://github.com/daleobrien/maze/blob/master/my_maze.pdf

The ASCI version produces;

    python maze_ascii.py

    ┌─┐ ┌─┐ ┌─┐ ┌── ─── ──┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐
    │ │ │ │ │ │ └── ─── ┐ │ │ │ │ │ │ │ │ │
    │ └ ┘ └ ┘ └ ─── ─── ┴─┴ ┘ └ ┘ └ ┤ ├ ┘ │
    │ ┌ ─── ─── ─── ─── ┬─┬ ┐ ┌ ┐ ┌ ┤ ├ ──┘
    │ │ ┌─┐ ┌─┐ ┌── ──┐ │ └ ┴─┴ ┘ │ │ │ ┌─┐
    └─┘ │ │ │ │ │ ┌ ┐ │ └── ┬─┬ ┐ │ │ │ │ │
    ┌── ┘ │ │ └ ┴─┴ ┘ │ ┌─┐ │ └ ┤ ├ ┘ │ │ │
    │ ┌ ──┘ │ ┌ ┬─┬ ──┘ │ │ └── ┤ ├ ┐ │ │ │
    │ │ ┌─┐ │ │ │ │ ┌── ┤ ├ ──┐ │ │ │ └ ┘ │
    │ │ │ │ └─┘ │ │ │ ┌ ┤ ├ ──┘ │ │ └── ┐ │
    │ └ ┴─┴ ─── ┴─┴ ┘ │ │ └ ─── ┴─┴ ──┐ │ │
    │ ┌ ┬─┬ ┐ ┌ ┬─┬ ┐ │ └── ┐ ┌ ┬─┬ ┐ │ └─┘
    │ └ ┘ └ ┤ ├ ┘ │ │ │ ┌── ┴─┴ ┘ └ ┤ ├ ──┐
    │ ┌ ─── ┤ ├ ┐ │ └─┘ │ ┌ ┬─┬ ─── ┤ ├ ──┘
    │ │ ┌─┐ │ └ ┴─┴ ─── ┤ ├ ┘ └ ──┐ │ └ ──┐
    └─┘ │ │ │ ┌ ┬─┬ ┐ ┌ ┤ ├ ┐ ┌ ──┘ │ ┌ ──┘
    ┌── ┤ ├ ┘ │ │ └ ┤ ├ ┘ └ ┤ ├ ─── ┴─┴ ──┐
    │ ┌ ┤ ├ ──┘ │ ┌ ┤ ├ ─── ┤ ├ ┐ ┌ ┬─┬ ──┘
    │ │ │ └ ─── ┘ │ │ │ ┌── ┘ │ │ │ │ └ ──┐
    └─┘ └── ─── ──┘ └─┘ └── ──┘ └─┘ └── ──┘

Requirements
===
For the maze_pdf.py, you will need to install reportlab.

    pip install reportlab
