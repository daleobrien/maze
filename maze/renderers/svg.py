from inspect import trace
from math import sqrt, asin, pi, ceil, sin, cos
from pickle import TRUE

QUARTER = pi / 2
HALF = pi
THREE_QUARTER = 3 * pi / 2
FULL = 2 * pi


class SVGPath(object):

    def __init__(self, colour, stroke_width, opacity, s, draw_with_curves=True):
        print("draw_with_curves", draw_with_curves)
        self.svg = ''
        self.dots = ''
        self.colour = colour
        self.stroke_width = stroke_width
        self.opacity = opacity

        self.S = s
        self.S2 = s / 2.0
        g = s * 0.2
        self.B = s - g
        k = 0.5

        n = -(g / k) + 0.5 * (s - sqrt((g *
                                        (4.0 * g - 3.0 * g * k + 2 * k * s)) / k))

        r = g / k
        q = n + r
        v = (g * (-1 + k)) / k

        theta = asin((2.0 * g - 2.0 * g * k + k * s) /
                     (2.0 * g - g * k + k * s))

        delta = theta - pi / 2.0

        self.QUARTER = pi / 2
        # inside loop
        self.A = g
        self.A2 = g / 2.0
        self.B = s - g
        self.B2 = s - g / 2.0
        self.R3 = s / 2.0 - g / 2.0
        self.R4 = s / 2.0 - g

        self.G = g
        self.N = n
        self.R = r
        self.R2 = s - g - g
        self.S = s
        self.S2 = s / 2
        self.Q = q
        self.V = v
        self.delta = delta
        self.theta = theta

        self.draw_with_curves = draw_with_curves

    def path(self):
        return f"""<path opacity="{self.opacity}" stroke-width="{self.stroke_width}" stroke="{self.colour}" d="{self.svg}"></path> {self.dots}"""

    def dot(self, x, y):
        a = self.round(x + self.S2)
        b = self.round(y + self.S2)
        r = self.round(self.S / 3.0)

        self.dots += f"""<circle cx="{a}" cy="{b}" r="{r}" fill-opacity="1.0" stroke-opacity="0" fill="#E51919" />"""

    def polar(self, x, y, radius, angle):
        return [x + (radius * cos(angle)), y + (radius * sin(angle))]

    def posAngle(self, angle):
        return angle + FULL if angle < 0 else angle

    def polarToCartesian(self, x, y, radius, angle):
        return [self.round(x + (radius * cos(angle))), self.round(y + (radius * sin(angle)))]

    def round(self, x):
        # round and strip trialing zeros after the decimal point
        s = f"{x:.2f}"
        if s.find('.') > -1:
            while s.endswith('0'):
                s = s[:-1]
            if s.endswith('.'):
                s = s[:-1]
        return s

    def a(self, x, y, radius, startAngle, endAngle, dir=1):
        _s = self.posAngle(startAngle)
        _e = self.posAngle(endAngle)
        [a, b] = self.polar(x, y, radius, _s)
        [c, d] = self.polar(x, y, radius, _e)

        diff = _e - _s
        large = 1 - dir if 0 < diff and diff <= pi else dir

        self.svg += f"""L{self.round(a)} {self.round(b)} A {self.round(radius)} {self.round(radius)} 0 {large} {dir} {self.round(c)} {self.round(d)} """

    def m(self, x, y):
        self.svg += f"M {self.round(x)} {self.round(y)} "

    def l(self, x, y):
        self.svg += f"L {self.round(x)} {self.round(y)} "

    def ml(self, a, b, c, d):
        self.m(a, b)
        self.l(c, d)

    def mh(self, a, b, x):
        self.ml(a, b, a + x, b)

    def mv(self, a, b, y):
        self.ml(a, b, a, b + y)

    def h(self, x, y, v):
        self.ml(x, y + v, x + self.S, y + v)

    def v(self, x, y, h):
        self.ml(x + h, y, x + h, y + self.S)


class SVGPathTrace(SVGPath):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TRAIL_CELLS = {
            't': {'l': self.t9, 'r': self.t5, 'b': self.t3},
            'l': {'t': self.t9, 'r': self.tc, 'b': self.ta},
            'r': {'l': self.tc, 't': self.t5, 'b': self.t6},
            'b': {'l': self.ta, 'r': self.t6, 't': self.t3}
        }
        self.TRAIL_LAST = {
            'r': self.t4,
            'l': self.t8,
            'b': self.t2,
            't': self.t1}

    def render(self, solution):

        # self.TILES(cell)(x, y)
        pass

    def t1(self, x, y):
        # │
        # .
        self.mv(x + self.S2, y, self.S2)

    def t2(self, x, y):
        # .
        # │
        self.mv(x + self.S2, y + self.S, -self.S2)

    def t4(self, x, y):
        # .-
        self.mh(x + self.S, y + self.S2, -self.S2)

    def t8(self, x, y):
        # -.
        self.mh(x, y + self, self)

    def t5(self, x, y):
        # Medium arc
        # └─
        self.m(x + self.S, y + self.S2)
        self.a(x + self.B2, y + self.A2, self.R3, QUARTER, HALF)
        self.l(x + self.S2, y)

    def t6(self, x, y):
        # ┌─
        self.m(x + self.S, y + self.S2)
        self.a(x + self.B2, y + self.B2, self.R3, THREE_QUARTER, HALF, 0)
        self.l(x + self.S2, y + self.S)

    def t9(self, x, y):
        # ─┘
        self.m(x + self.S2, y)
        self.a(x + self.A2, y + self.A2, self.R3, 0, QUARTER)
        self.l(x, y + self.S2)

    def ta(self, x, y):
        # ─┐
        self.m(x, y + self.S2)
        self.a(x + self.A2, y + self.B2, self.R3, THREE_QUARTER, HALF)
        self.l(x + self.S2, y + self.S)

    def t3(self, x, y):
        # │
        # │
        self.v(x, y, self.S2)

    def tc(self, x, y):
        # ───
        self.h(x, y, self.S2)

    def tg(self, x, y):
        # Outside to A/B
        self.mh(x, y + self.S2, self.A)
        self.mh(x + self.S, y + self.S2, -self.A)
        # Inside to A/B (faint)
        self.mh(x + self.A, y + self.S2, self.R4)
        self.mh(x + self.B, y + self.S2, -self.R4)

    def th(self, x, y):
        # Outside to A/B
        self.mv(x + self.S2, y, self.A)
        self.mv(x + self.S2, y + self.S, -self.A)
        # Inside to A/B (faint)
        self.mv(x + self.S2, y + self.A, self.R4)
        self.mv(x + self.S2, y + self.B, -self.R4)


class SVGPathMazeWalls(SVGPath):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TILES = {1: self.c1, 2: self.c2, 3: self.c3, 4: self.c4, 5: self.c5, 6: self.c6,
                      7: self.c7, 8: self.c8, 9: self.c9, 10: self.ca, 11: self.cb, 12: self.cc,
                      13: self.cd, 14: self.ce, 15: self.cf, 19: self.cg, 28: self.ch}

    def render(self, grid):
        left_margin = 0
        top_margin = 0

        for j, row in enumerate(grid):
            y = top_margin + j * self.S

            for i, cell in enumerate(row):
                x = left_margin + i * self.S

                if (i == 0 and j == len(grid) - 1) or (i == len(row) - 1 and j == 0):
                    self.dot(x, y)
                else:
                    self.TILES[cell](x, y)

    def s0(self, x, y, radius=None):
        # ┘
        self.m(x + self.A, y)
        if self.draw_with_curves:
            if radius is None:
                radius = self.A
            self.a(x, y, radius, 0, QUARTER)
        else:
            self.l(x + self.A, y + self.A)
        self.l(x, y + self.A)

    def s1(self, x, y, radius=None):
        # ┐
        self.m(x, y + self.B)
        if self.draw_with_curves:
            if radius is None:
                radius = self.A
            self.a(x, y + self.S, radius, THREE_QUARTER, FULL)
        else:
            self.l(x + self.A, y + self.B)
        self.l(x + self.A, y + self.S)

    def s2(self, x, y, radius=None):
        # └
        self.m(x + self.S, y + self.A)
        if self.draw_with_curves:
            if radius is None:
                radius = self.A
            self.a(x + self.S, y, radius, QUARTER, HALF)
        else:
            self.l(x + self.B, y + self.A)
        self.l(x + self.B, y)

    def s3(self, x, y, radius=None):
        # ┌
        self.m(x + self.S, y + self.B)
        if self.draw_with_curves:
            if radius is None:
                radius = self.A
            self.a(x + self.S, y + self.S, radius, THREE_QUARTER, HALF, 0)
        else:
            self.l(x + self.B, y + self.B)
        self.l(x + self.B, y + self.S)

    def c1(self, x, y):
        # │ │
        # └─┘
        self.mv(x + self.B, y, self.Q)
        if self.draw_with_curves:
            self.a(x + self.S - self.V, y + self.N + self.R,
                   self.R, HALF, HALF + self.delta, 0)
            self.a(x + self.S2, y + self.S2, self.S2 - self.G / 2,
                   self.theta - QUARTER, THREE_QUARTER - self.theta)
            self.a(x + self.V, y + self.N + self.R, self.R, QUARTER -
                   self.theta, THREE_QUARTER + self.theta - self.delta, 0)
        else:
            self.l(x + self.B, y + self.B)
            self.l(x + self.A, y + self.B)
        self.l(x + self.G, y)

    def c2(self, x, y):
        # ┌─┐
        # │ │
        self.m(x + self.B, y + self.S)
        if self.draw_with_curves:
            self.a(x + self.S - self.V, y + self.S - self.N -
                   self.R, self.R, HALF, HALF - self.delta)
            self.a(x + self.S2, y + self.S2, self.S2 - self.G / 2.0,
                   QUARTER - self.theta, self.theta - THREE_QUARTER, 0)
            self.a(x + self.V, y + self.S - self.N - self.R, self.R,
                   THREE_QUARTER + self.theta, THREE_QUARTER + self.theta - self.delta)
        else:
            self.l(x + self.B, y + self.A)
            self.l(x + self.A, y + self.A)
        self.l(x + self.A, y + self.S)

    def c4(self, x, y):
        # ┌──
        # └──
        self.m(x + self.S, y + self.B)
        if self.draw_with_curves:
            self.a(x + self.S - self.N - self.R, y + self.S - self.V,
                   self.R, THREE_QUARTER, THREE_QUARTER + self.delta, 0)
            self.a(x + self.S2, y + self.S2, self.S2 - self.G / 2.0,
                   QUARTER + self.delta, QUARTER + self.delta - 2 * self.theta)
            self.a(x + self.S - self.N - self.R, y + self.V, self.R,
                   HALF - self.theta, HALF - self.theta + self.delta, 0)
        else:
            self.l(x + self.G, y + self.B)
            self.l(x + self.A, y + self.A)

        self.l(x + self.S, y + self.A)

    def c8(self, x, y):
        # ──┐
        # ──┘
        self.m(x, y + self.B)
        if self.draw_with_curves:
            self.a(x + self.N + self.R, y + self.S - self.V, self.R,
                   THREE_QUARTER, THREE_QUARTER - self.delta)
            self.a(x + self.S2, y + self.S2, self.S2 - self.G / 2.0,
                   QUARTER - self.delta, QUARTER - self.delta + 2.0 * self.theta, 0)
            self.a(x + self.N + self.R, y + self.V, self.R,
                   self.theta, self.theta - self.delta)
        else:
            self.l(x + self.B, y + self.B)
            self.l(x + self.B, y + self.A)
        self.l(x, y + self.A)

    def c5(self, x, y):
        # │ └
        # └──
        # Small arc
        self.s2(x, y)

        # Big arc
        self.m(x + self.S, y + self.B)
        if self.draw_with_curves:
            self.a(x + self.B, y + self.A, self.R2, QUARTER, HALF)
        else:
            self.l(x + self.A, y + self.B)
        self.l(x + self.A, y)

    def c6(self, x, y):
        # ┌──
        # │ ┌
        self.s3(x, y)
        self.m(x + self.S, y + self.A)
        if self.draw_with_curves:
            self.a(x + self.B, y + self.B, self.R2, THREE_QUARTER, HALF, 0)
        else:
            self.l(x + self.A, y + self.A)
        self.l(x + self.A, y + self.S)

    def c9(self, x, y):
        # ┘ │
        # ──┘
        self.s0(x, y)
        self.m(x + self.B, y)
        if self.draw_with_curves:
            self.a(x + self.A, y + self.A, self.R2, 0, QUARTER)
        else:
            self.l(x + self.B, y + self.B)
        self.l(x, y + self.B)

    def ca(self, x, y):
        # ──┐
        # ┐ │
        self.s1(x, y)
        self.m(x, y + self.A)
        if self.draw_with_curves:
            self.a(x + self.A, y + self.B, self.R2, THREE_QUARTER, FULL)
        else:
            self.l(x + self.B, y + self.A)
        self.l(x + self.B, y + self.S)

    def c7(self, x, y):
        # │ └
        # │ ┌
        self.v(x, y, self.A)
        self.s2(x, y)
        self.s3(x, y)

    def cb(self, x, y):
        # ┘ │
        # ┐ │
        self.v(x, y, self.B)
        self.s0(x, y)
        self.s1(x, y)

    def c3(self, x, y):
        # │ │
        # │ │
        self.v(x, y, self.A)
        self.v(x, y, self.B)

    def cc(self, x, y):
        # ───
        # ───
        self.h(x, y, self.A)
        self.h(x, y, self.B)

    def cd(self, x, y):
        # ┘ └
        # ───
        self.h(x, y, self.B)
        self.s0(x, y)
        self.s2(x, y)

    def ce(self, x, y):
        # ───
        # ┐ ┌
        self.h(x, y, self.A)
        self.s1(x, y)
        self.s3(x, y)

    def cf(self, x, y):
        # ┘ └
        # ┐ ┌
        self.s0(x, y)
        self.s1(x, y)
        self.s2(x, y)
        self.s3(x, y)

    def cg(self, x, y):
        # ┤ ├
        # ┤ ├
        self.v(x, y, self.A)
        self.v(x, y, self.B)

        self.mh(x, y + self.A, self.A)
        self.mh(x, y + self.B, self.A)

        self.mh(x + self.S, y + self.A, self.B - self.S)
        self.mh(x + self.S, y + self.B, self.B - self.S)

    def ch(self, x, y):
        # ┴─┴
        # ┬─┬
        self.h(x, y, self.A)
        self.h(x, y, self.B)

        self.mv(x + self.A, y, self.A)
        self.mv(x + self.B, y, self.A)

        self.mv(x + self.A, y + self.B, self.S - self.B)
        self.mv(x + self.B, y + self.B, self.S - self.B)


class SVG(object):

    def __init__(self, grid, options):

        # Map a 'draw' function to each kind of tile
        self.dots = ''

        width = options['width']
        height = options['height']
        use_A4 = options['use_A4']
        draw_with_curves = options['draw_with_curves']
        self.solution = options['solution']
        left_margin = 0
        print(options)
        print(self.solution)

        dpi = 72
        if use_A4:
            page_width = 8.3 * dpi
            page_height = 11.7 * dpi
            # landscape
            page_height = 8.3 * dpi
            page_width = 11.7 * dpi
        else:
            # US Letter
            page_width = 8.5 * dpi
            page_height = 11.0 * dpi

        # cells must be square, it's the math!, I'm not doing it again.
        # so scale the width if the height will go over the page
        if (float(height) / width) > (page_height / page_width):
            width = ceil(page_width / page_height * height)

        s = (page_width - 2 * left_margin) / width
        self.stroke_width = 2

        self.p = SVGPathMazeWalls(
            '#000000', self.stroke_width, '1.0', s, draw_with_curves)  # Maze walls
        self.t = SVGPathTrace('#E51919', 5, '1.0', s,
                              draw_with_curves)  # solution
        self.f = SVGPathTrace('#E51919', 5, '0.1', s,
                              draw_with_curves)  # faint solution lines

        self.width = width
        self.height = height

        self.p.render(grid)

    def create_solution(self):

        for idx, trail in enumerate(self.solution):
            # current
            [x, y] = trail

            if idx == len(self.solution) - 1:
                # last cell
                [x_p, y_p] = trail[idx - 1]
                from_d = direction(x - x_p, y - y_p)
                TRAIL_LAST[from_d](x * S, y * S)

                t.dot(x * S, y * S, S / 5)

            else:
                [x_n, y_n] = trail[idx + 1]

                if (idx == 0):
                    # First cell
                    if (x == x_n):
                        t1(x * S, y * S)
                    else:
                        t4(x * S, y * S)

                else:
                    [x_p, y_p] = trail[idx - 1]
                    from_d = direction(x - x_p, y - y_p)
                    to_d = direction(x - x_n, y - y_n)

                    t_cell = TRAIL_CELLS[from_d][to_d]
                    current_cell = grid[y][x]
                    if (t_cell == tc and current_cell == cg):
                        tg(x * S, y * S)
                    elif (t_cell == t3 and current_cell == ch):
                        th(x * S, y * S)
                    else:
                        t_cell(x * S, y * S)

    def image(self):
        return f"""<svg id="maze" width="{self.width}" height="{self.height}" stroke-width="{self.stroke_width}" fill-opacity="0.0" stroke="#000">
          {self.p.path()}
          {self.t.path()}
          {self.f.path()}
          {self.dots}
         </svg>"""


def render(grid, options):
    svg = SVG(grid, options)
    return svg.image()
