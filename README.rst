maze
====

Maze generator with crossing;

    python maze_pdf.py    

will produce a pdf, much like this one by default;

.. image:: /daleobrien/maze/raw/master/maze.gif


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
