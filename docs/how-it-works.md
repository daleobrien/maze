# How it works

[Back to the README](../README.md)

maze makes **weave mazes**: mazes with passages that pass both over and under
other passages. The technique was described by Robin Houston. It works by
first decorating the blank grid with the over-and-under crossings, then using
Kruskal's algorithm to fill out the rest of the grid. Kruskal's is very
well suited to this, since it treats the cells as separate sets and joins them
together. `-d` sets how many crossings are placed first, and `-L` leaves one
loop in.

The program was first ported from <https://gist.github.com/856138>.

## The code

- `maze/maze.py`: the command line (with docopt), and making and solving the
  maze.
- `maze/renderers/svg.py`: SVG, with curved or straight corridors and the
  solution.
- `maze/renderers/pdf.py`: PDF, with ReportLab.
- `maze/renderers/text.py`: text, for the terminal.

## The Rust version

[maze-rs](https://github.com/daleobrien/maze-rs) is a port to Rust, with the
same command line and the same drawing, many times faster, and with more:
solutions in PDFs, a hand-drawn ink style and other styles, and a library that
builds for WebAssembly. Its maze ids give different mazes from these.
[maze.do.id.au](https://maze.do.id.au) uses it to play mazes in the browser.
