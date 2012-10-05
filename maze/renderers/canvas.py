# -*- coding: utf-8 -*-
from mako.template import Template
from math import sqrt, asin, pi, ceil


'''
This is slow, decided to use js.py instead, e.g. generate higherlevel drawing
commands to be inserted into a html canvas.
'''


# generate canvas commands for html
def render(grid, options):

    QUARTER = pi / 2.0
    HALF = pi
    THREE_QUARTER = 3.0 * pi / 2.0
    FULL = 2.0 * pi

    draw_with_curves = options['draw_with_curves']
    width = options['width']
    height = options['height']
    use_A4 = options['use_A4']

    if use_A4:
        page_width = 8.3 * 72
        page_height = 11.7 * 72
    else:
        page_width = 8.5 * 72
        page_height = 11.0 * 72

    left_margin = 0
    top_margin = 0

    # cells must be square, it's the math!, I'm not doing it again.
    # so scale the width if the height will go over the page
    if (float(height) / width) > (page_height / page_width):
        width = ceil(page_width / page_height * height)

    s = (page_width - 2 * left_margin) / width
    g = s * 0.2

    k = 0.5

    n = -(g / k) + 0.5 * (s - sqrt((g *
        (4.0 * g - 3.0 * g * k + 2 * k * s)) / k))

    r = g / k
    q = n + r
    v = (g * (-1 + k)) / k

    theta = asin((2.0 * g - 2.0 * g * k + k * s) /
        (2.0 * g - g * k + k * s))

    delta = theta - QUARTER

    a = g
    b = s - g

    s_shape_00 = """p.moveTo(${x+a},${y});
                    % if draw_with_curves:
                        p.arc(${x},${y},${a},0,${QUARTER},false);
                    % else:
                        p.lineTo(${a+x},${a+y});
                    % endif
                    p.lineTo(${x},${a+y});"""

    s_shape_01 = """p.moveTo(${x},${y+b});
                    % if draw_with_curves:
                        p.arc(${x},${s+y},${a},${THREE_QUARTER},0,false);
                    % else:
                        p.lineTo(${a+x},${b+y});
                    % endif
                    p.lineTo(${a+x},${s+y});"""

    s_shape_10 = """p.moveTo(${x+s},${y+a});
                    % if draw_with_curves:
                        p.arc(${x+s},${y},${a},${QUARTER},${HALF},false);
                    % else:
                        p.lineTo(${x+b},${y+a});
                    % endif
                    p.lineTo(${x+b},${y});"""

    s_shape_11 = """p.moveTo(${x+s},${y+b});
                    % if draw_with_curves:
                        p.arc(${x+s},${y+s},${a},${THREE_QUARTER},${HALF},
                            true);
                    % else:
                        p.lineTo(${x+b},${y+b});
                    % endif
                    p.lineTo(${x+b},${y+s});"""

    # │ │
    # └─┘
    cell_1 = """p.moveTo(${x+b},${y});
                % if draw_with_curves:
                    p.lineTo(${x+b},${y+q});
                    p.arc(${x+s-v},${y+n+r},${r},${HALF},${HALF+delta},true);
                    p.arc(${x+s/2},${y+s/2},${s/2-g/2},
                        ${theta-QUARTER},${THREE_QUARTER-theta},false);
                    p.arc(${x+v},${y+n+r},${r},${QUARTER-theta},
                        ${THREE_QUARTER+theta-delta},true);
                % else:
                    p.lineTo(${x+b},${y+b});
                    p.lineTo(${x+a},${y+b});
                % endif
                p.lineTo(${x+g},${y});"""

    # ┌─┐
    # │ │
    cell_2 = """p.moveTo(${x+b},${y+s});
                % if draw_with_curves:
                    p.arc(${x+s-v},${y+s-n-r},${r},
                        ${HALF},${HALF-delta},false);
                    p.arc(${x+s/2},${y+s/2},${s/2-g/2},
                        ${QUARTER-theta},${theta-THREE_QUARTER},true);
                    p.arc(${x+v},${y+s-n-r},${r},
                        ${THREE_QUARTER+theta},${THREE_QUARTER+theta-delta},
                        false);
                % else:
                    p.lineTo(${x+b},${y+a});
                    p.lineTo(${x+a},${y+a});
                % endif
                p.lineTo(${x+a},${y+s});"""

    # ┌──
    # └──
    cell_4 = """p.moveTo(${x+s},${y+b});
                % if draw_with_curves:
                    p.arc(${x+s-n-r},${y+s-v},${r},
                        ${THREE_QUARTER},${THREE_QUARTER+delta},true);
                    p.arc(${x+s/2},${y+s/2},${s/2-g/2},
                        ${QUARTER+delta},${QUARTER+delta-2*theta},false);
                    p.arc(${x+s-n-r},${y+v},${r},
                        ${HALF-theta},${HALF-theta+delta},true);
                % else:
                    p.lineTo(${x+g},${y+b});
                    p.lineTo(${x+a},${y+a});
                % endif
                p.lineTo(${x+s},${y+a});"""

    # ──┐
    # ──┘
    cell_8 = """p.moveTo(${x},${y+b});
                % if draw_with_curves:
                    p.arc(${x+n+r},${y+s-v},${r},
                        ${THREE_QUARTER},${THREE_QUARTER-delta},false);
                    p.arc(${x+s/2},${y+s/2},${s/2-g/2},
                        ${QUARTER-delta},${QUARTER-delta+2*theta},true);
                    p.arc(${x+n+r},${y+v},${r},${theta},${theta-delta},false);
                % else:
                    p.lineTo(${x+b},${y+b});
                    p.lineTo(${x+b},${y+a});
                % endif
                p.lineTo(${x},${y+a});"""

    #  │ └
    #  └──
    cell_5 = """p.moveTo(${x+s},${y+b});
                % if draw_with_curves:
                    % if start:
                        p.arc(${x+(a+b)/2},${y+(a+b)/2},${(b-a)/2},
                            ${QUARTER},${HALF},false);
                    % else:
                        p.arc(${x+b},${y+a},${b-a},${QUARTER},${HALF},false);
                    % endif
                % else:
                    p.lineTo(${x+a},${y+b});
                % endif
                p.lineTo(${x+a},${y});
                """ + s_shape_10

    # ┌──
    # │ ┌
    cell_6 = """p.moveTo(${x+s},${y+a});
                % if draw_with_curves:
                    p.arc(${x+a+b},${y+a+b},${b},
                        ${THREE_QUARTER},${HALF},true);
                % else:
                    p.lineTo(${x+a},${y+a});
                % endif
                p.lineTo(${x+a},${y+s});""" + s_shape_11

    #  ┘ │
    #  ──┘
    cell_9 = """p.moveTo(${x+b},${y});
                % if draw_with_curves:
                    p.arc(${x+a},${y+a},${b-a},0,${QUARTER},false);
                % else:
                    p.lineTo(${x+b},${y+b});
                % endif
                p.lineTo(${x},${y+b});""" + s_shape_00

    # ──┐
    # ┐ │
    cell_10 = """p.moveTo(${x},${y+a});
                % if draw_with_curves:
                    % if end:
                        p.arc(${x+(a+b)/2},${y+(a+b)/2},${(b-a)/2},
                            ${THREE_QUARTER},${FULL},false);
                    % else:
                        p.arc(${x+a},${y+b},${b-a},
                            ${THREE_QUARTER},${FULL}, false);
                    % endif
                % else:
                    p.lineTo(${x+b},${y+a});
                % endif
                p.lineTo(${x+b},${y+s});
                """ + s_shape_01

    # │ └
    # │ ┌
    cell_7 = """p.moveTo(${x+a},${y+s});
                p.lineTo(${x+a},${y});""" + s_shape_10 + s_shape_11

     # ┘ │
     # ┐ │
    cell_11 = """p.moveTo(${x+b},${y+s});
                 p.lineTo(${x+b},${y});""" + s_shape_00 + s_shape_01

    # ┘ └
    # ───
    cell_13 = """p.moveTo(${x},${y+b});
                 p.lineTo(${x+s},${y+b});""" + s_shape_00 + s_shape_10

    # ───
    # ┐ ┌
    cell_14 = """p.moveTo(${x},${y+a});
                 p.lineTo(${x+s},${y+a});""" + s_shape_01 + s_shape_11

    # ┘ └
    # ┐ ┌
    cell_15 = s_shape_00 + s_shape_01 + s_shape_10 + s_shape_11

    # │ │
    # │ │
    cell_3 = """p.moveTo(${x+a},${y+s});
                p.lineTo(${x+a},${y});
                p.moveTo(${x+b},${y+s});
                p.lineTo(${x+b},${y});"""

    # ───
    # ───
    cell_12 = """p.moveTo(${x},${y+b});
                 p.lineTo(${x+s},${y+b});
                 p.moveTo(${x},${y+a});
                 p.lineTo(${x+s},${y+a});"""

    # ┤ ├
    # ┤ ├
    cell_19 = """p.moveTo(${x+a},${y+s});
                 p.lineTo(${x+a},${y});
                 p.moveTo(${x+b},${y+s});
                 p.lineTo(${x+b},${y});

                 p.moveTo(${x},${y+a});
                 p.lineTo(${x+a},${y+a});
                 p.moveTo(${x},${y+b});
                 p.lineTo(${x+a},${y+b});

                 p.moveTo(${x+s},${y+a});
                 p.lineTo(${x+b},${y+a});
                 p.moveTo(${x+s},${y+b});
                 p.lineTo(${x+b},${y+b});"""

    # ┴─┴
    # ┬─┬
    cell_28 = """p.moveTo(${x},${y+b});
                 p.lineTo(${x+s},${y+b});
                 p.moveTo(${x},${y+a});
                 p.lineTo(${x+s},${y+a});

                 p.moveTo(${x+a},${y+a});
                 p.lineTo(${x+a},${y});
                 p.moveTo(${x+a},${y+b});
                 p.lineTo(${x+a},${y+s});

                 p.moveTo(${x+b},${y+a});
                 p.lineTo(${x+b},${y});
                 p.moveTo(${x+b},${y+b});
                 p.lineTo(${x+b},${y+s});"""

    parameters = {'draw_with_curves': draw_with_curves,
                  'a': a,
                  'b': b,
                  'g': g,
                  'n': n,
                  'r': r,
                  's': s,
                  'q': q,
                  'v': v,
                  'x': 100,
                  'y': 300,
                  'QUARTER': QUARTER,
                  'HALF': HALF,
                  'THREE_QUARTER': THREE_QUARTER,
                  'FULL': FULL,
                  'delta': delta,
                  'theta': theta}

    TILES = {1: cell_1,
             2: cell_2,
             3: cell_3,
             4: cell_4,
             5: cell_5,
             6: cell_6,
             7: cell_7,
             8: cell_8,
             9: cell_9,
             10: cell_10,
             11: cell_11,
             12: cell_12,
             13: cell_13,
             14: cell_14,
             15: cell_15,
             19: cell_19,
             28: cell_28
             }

    js = ""
    for j, row in enumerate(grid):
        # upper/lower rows
        for i, cell in enumerate(row):

            parameters['x'] = left_margin + i * s
            parameters['y'] = top_margin + j * s

            # mark start and end
            start = False
            end = False
            if (i == 0 and j == height - 1):
                start = True

            if (i == width - 1 and j == 0):
                end = True

            parameters['end'] = end
            parameters['start'] = start

            js += Template(TILES[cell]).render(**parameters)

    # compress a little
    js = js.replace(" ", "").replace("\n", "")

    return js
