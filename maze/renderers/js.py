# generate some a svg for a html
import os
from math import asin, ceil, pi, sqrt

import rjsmin
from mako.template import Template


def render(grid, options):

    draw_with_curves = options['draw_with_curves']
    width = options['width']
    height = options['height']
    use_A4 = options['use_A4']

    dpi = 72
    if use_A4:
        page_width = 8.3 * dpi
        page_height = 11.7 * dpi
        # landscape
        page_height = 8.3 * dpi
        page_width = 11.7 * dpi
    else:  # US Letter
        page_width = 8.5 * dpi
        page_height = 11.0 * dpi

    left_margin = 0
    top_margin = 0

    # cells must be square, it's the math!, I'm not doing it again.
    # so scale the width if the height will go over the page
    if (float(height) / width) > (page_height / page_width):
        width = ceil(page_width / page_height * height)

    s = (page_width - 2 * left_margin) / width
    g = s * 0.2
    # stroke = s / 7.0

    k = 0.5

    n = -(g / k) + 0.5 * (s - sqrt((g *
                                    (4.0 * g - 3.0 * g * k + 2 * k * s)) / k))

    r = g / k
    q = n + r
    v = (g * (-1 + k)) / k

    theta = asin((2.0 * g - 2.0 * g * k + k * s) /
                 (2.0 * g - g * k + k * s))

    delta = theta - pi / 2.0

    # inside loop
    a = g
    a2 = a / 2.0
    b = s - a
    b2 = s - a2
    r4 = s / 2.0 - a

    TILES = {1: 'c1', 2: 'c2', 3: 'c3', 4: 'c4', 5: 'c5', 6: 'c6',
             7: 'c7', 8: 'c8', 9: 'c9', 10: 'ca', 11: 'cb', 12: 'cc',
             13: 'cd', 14: 'ce', 15: 'cf', 19: 'cg', 28: 'ch'}
    ports = {'c1': 1}

    js = ""

    s_x_s = []
    s_y_s = []

    # Since the x & y repeat, make some vars
    for j, row in enumerate(grid):
        y = top_margin + j * s
        s_y_s.append(f"{y:0.2f}")

    for i, cell in enumerate(row):
        x = left_margin + i * s
        s_x_s.append(f"{x:0.2f}")

    s_y_s = f"const y_s =[{','.join(s_y_s)}]"
    s_x_s = f"const x_s =[{','.join(s_x_s)}]"

    nl = ',\n     '
    rows = []

    for j, row in enumerate(grid):
        js_row = []
        for i, cell in enumerate(row):
            js_row.append(TILES[cell])
        rows.append(f"[{','.join(js_row)}]")

    grid = f"const grid = [{','.join(rows)}]"

    folder, _ = os.path.split(os.path.realpath(__file__))
    svg_template = open(os.path.join(folder, 'js/render.mako.js')).read()

    js_content = Template(svg_template).render(a=a, a2=a2, b=b, b2=b2, g=g, n=n, r=r, s=s, q=q, v=v, delta=delta,
                                               theta=theta, grid=grid, s2=s/2.0, r2=b-a, r3=(s/2.0-a/2.0), r4=r4,
                                               width=options['width'], height=height, s_x_s=s_x_s, s_y_s=s_y_s)

    js_content = rjsmin.jsmin(js_content)

    return js_content

#
