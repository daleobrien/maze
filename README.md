maze
====

Maze generator with crossing.

    python maze_pdf.py    

![my_maze.pdf](sample_maze.jpg "my_maze.pdf")
![my_maze.pdf](https://github.com/daleobrien/maze/blob/master/sample_maze.jpg "my_maze.pdf")
![my_maze.pdf](https://github.com/daleobrien/maze/sample_maze.jpg "my_maze.pdf")
![my_maze.pdf](//github.com/daleobrien/maze/sample_maze.jpg "my_maze.pdf")
![my_maze.pdf](/daleobrien/maze/sample_maze.jpg "my_maze.pdf")
![my_maze.pdf](/maze/sample_maze.jpg "my_maze.pdf")
https://github.com/daleobrien/maze/blob/master/sample_maze.jpg

Will generate a maze much like this,

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
