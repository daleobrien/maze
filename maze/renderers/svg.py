from math import sqrt, asin, pi, ceil, sin, cos

QUARTER = pi / 2
HALF = pi
THREE_QUARTER = 3 * pi / 2
FULL = 2 * pi


class SVG(object):

    def __init__(self, grid, options):

        # Map a 'draw' function to each kind of tile
        self.TILES = {1: self.c1, 2: self.c2, 3: self.c3, 4: self.c4, 5: self.c5, 6: self.c6,
                      7: self.c7, 8: self.c8, 9: self.c9, 10: self.ca, 11: self.cb, 12: self.cc,
                      13: self.cd, 14: self.ce, 15: self.cf, 19: self.cg, 28: self.ch}

        self.svg = ''
        self.dots = ''

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
        self.A = g
        self.B = s - g

        self.WIDTH = width
        self.HEIGHT = height

        self.G = g
        self.N = n
        self.R = r
        self.S = s
        self.Q = q
        self.V = v
        self.delta = delta
        self.theta = theta

        self.stroke_width = 1
        if width < 10:
            self.stroke_width = 5
        elif width < 30:
            self.stroke_width = 3
        elif width < 50:
            self.stroke_width = 2

        for j, row in enumerate(grid):
            y = top_margin + j * s

            for i, cell in enumerate(row):
                x = left_margin + i * s

                if (i == 0 and j == len(grid) - 1) or (i == len(row)-1 and j == 0):
                    self.dot(x, y)
                else:
                    self.TILES[cell](x, y)

    def image(self):
        return f"""<svg id=\"maze\" width=\"{self.WIDTH}\" height=\"{self.HEIGHT}\" stroke-width=\"{self.stroke_width}\" fill-opacity=\"0.0\" stroke=\"#000\">
          <path stroke-linecap=\"round\" 
            d=\"{self.svg}\"></path>
            {self.dots}
         </svg>"""

    def dot(self, x, y):
        _x = self.round(x + self.S / 2)
        _y = self.round(y + self.S / 2)
        _r = self.round(self.S / 3.0)

        self.dots += f"<circle cx=\"{_x}\" cy=\"{_y}\" r=\"{_r}\" fill-opacity=\"1.0\" stroke-opacity=\"0\" fill=\"#E51919\" />"

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

    def arc(self, x, y, radius, startAngle, endAngle, clockwise):
        _start = self.posAngle(startAngle)
        _end = self.posAngle(endAngle)

        ax, ay = self.polarToCartesian(x, y, radius, _start)
        bx, by = self.polarToCartesian(x, y, radius, _end)

        _dir = 0 if clockwise else 1

        diff = _end - _start
        largeArcFlag = 1 - _dir if 0 < diff <= HALF else _dir

        r = self.round(radius)

        self.svg += f"L{ax} {ay} A{r} {r} 0 {largeArcFlag} {_dir} {bx} {by}\n"

    def moveTo(self, x, y):
        self.svg += f"M{self.round(x)} {self.round(y)}\n"

    def lineTo(self, x, y):
        self.svg += f"L{self.round(x)} {self.round(y)}\n"

    def s_shape_00(self, x, y):
        self.moveTo(x + self.A, y)
        self.arc(x, y, self.A, 0, QUARTER, False)
        self.lineTo(x, y + self.A)

    def s_shape_01(self, x, y):
        self.moveTo(x, y + self.B)
        self.arc(x, y + self.S, self.A, THREE_QUARTER, FULL, False)
        self.lineTo(x + self.A, y + self.S)

    def s_shape_10(self, x, y):
        self.moveTo(x + self.S, y + self.A)
        self.arc(x + self.S, y, self.A, QUARTER, HALF, False)
        self.lineTo(x + self.B, y)

    def s_shape_11(self, x, y):
        self.moveTo(x + self.S, y + self.B)
        self.arc(x + self.S, y + self.S, self.A, THREE_QUARTER, HALF, True)
        self.lineTo(x + self.B, y + self.S)

    def c1(self, x, y):
        self.moveTo(x + self.B, y)
        self.lineTo(x + self.B, y + self.Q)

        self.arc(x + self.S - self.V, y + self.N + self.R,
                 self.R, HALF, HALF + self.delta, True)

        self.arc(
            x + self.S / 2, y + self.S / 2, self.S / 2 -
            self.G / 2, self.theta - QUARTER,
            THREE_QUARTER - self.theta, False)

        self.arc(
            x + self.V, y + self.N + self.R, self.R, QUARTER -
            self.theta, THREE_QUARTER + self.theta - self.delta,
            True)
        self.lineTo(x + self.G, y)

    def c2(self, x, y):
        self.moveTo(x + self.B, y + self.S)
        self.arc(x + self.S - self.V, y + self.S - self.N -
                 self.R, self.R, HALF, HALF - self.delta, False)
        self.arc(
            x + self.S / 2, y + self.S / 2, self.S / 2 - self.G /
            2, QUARTER - self.theta, self.theta - THREE_QUARTER,
            True)
        self.arc(
            x + self.V, y + self.S - self.N - self.R, self.R, THREE_QUARTER + self.theta,
            THREE_QUARTER + self.theta - self.delta, False)

        self.lineTo(x + self.A, y + self.S)

    def c3(self, x, y):
        self.moveTo(x + self.A, y + self.S)
        self.lineTo(x + self.A, y)
        self.moveTo(x + self.B, y + self.S)
        self.lineTo(x + self.B, y)

    def c4(self, x, y):
        self.moveTo(x + self.S, y + self.B)

        self.arc(
            x + self.S - self.N - self.R, y + self.S - self.V, self.R, THREE_QUARTER, THREE_QUARTER + self.delta, True)
        self.arc(
            x + self.S / 2, y + self.S / 2, self.S / 2 -
            self.G / 2, QUARTER + self.delta,
            QUARTER + self.delta - 2 * self.theta, False)
        self.arc(x + self.S - self.N - self.R, y + self.V, self.R, HALF -
                 self.theta, HALF - self.theta + self.delta, True)

        self.lineTo(x + self.S, y + self.A)

    def c5(self, x, y):
        self.s_shape_10(x, y)

        self.moveTo(x + self.S, y + self.B)
        self.arc(x + self.B, y + self.A, self.B -
                 self.A, QUARTER, HALF, False)
        self.lineTo(x + self.A, y)

    def c5_start(self, x, y):
        self.s_shape_10(x, y)

        self.moveTo(x + self.S, y + self.B)
        self.arc(x + (A + self.B) / 2, y + (A + self.B) / 2,
                 (B - self.A) / 2, QUARTER, HALF, False)

        self.lineTo(x + self.A, y)

    def c6(self, x, y):
        self.s_shape_11(x, y)

        self.moveTo(x + self.S, y + self.A)
        self.arc(x + self.A + self.B, y + self.A + self.B,
                 self.B, THREE_QUARTER, HALF, True)
        self.lineTo(x + self.A, y + self.S)

    def c7(self, x, y):
        self.moveTo(x + self.A, y + self.S)
        self.lineTo(x + self.A, y)

        self.s_shape_10(x, y)
        self.s_shape_11(x, y)

    def c8(self, x, y):
        self.moveTo(x, y + self.B)
        self.arc(x + self.N + self.R, y + self.S - self.V, self.R, THREE_QUARTER,
                 THREE_QUARTER - self.delta, False)
        self.arc(
            x + self.S / 2, y + self.S / 2, self.S / 2 -
            self.G / 2, QUARTER - self.delta,
            QUARTER - self.delta + 2 * self.theta, True)
        self.arc(x + self.N + self.R, y + self.V, self.R,
                 self.theta, self.theta - self.delta, False)

        self.lineTo(x, y + self.A)

    def c9(self, x, y):
        self.s_shape_00(x, y)

        self.moveTo(x + self.B, y)
        self.arc(x + self.A, y + self.A, self.B -
                 self.A, 0, QUARTER, False)
        self.lineTo(x, y + self.B)

    def ca(self, x, y):
        self.s_shape_01(x, y)

        self.moveTo(x, y + self.A)
        self.arc(x + self.A, y + self.B, self.B -
                 self.A, THREE_QUARTER, FULL, False)
        self.lineTo(x + self.B, y + self.S)

    def cb(self, x, y):
        self.moveTo(x + self.B, y + self.S)
        self.lineTo(x + self.B, y)

        self.s_shape_00(x, y)
        self.s_shape_01(x, y)

    def cc(self, x, y):
        self.moveTo(x, y + self.B)
        self.lineTo(x + self.S, y + self.B)
        self.moveTo(x, y + self.A)
        self.lineTo(x + self.S, y + self.A)

    def cd(self, x, y):
        self.moveTo(x, y + self.B)
        self.lineTo(x + self.S, y + self.B)

        self.s_shape_00(x, y)
        self.s_shape_10(x, y)

    def ce(self, x, y):
        self.moveTo(x, y + self.A)
        self.lineTo(x + self.S, y + self.A)

        self.s_shape_01(x, y)
        self.s_shape_11(x, y)

    def cf(self, x, y):
        self.s_shape_00(x, y)
        self.s_shape_01(x, y)
        self.s_shape_10(x, y)
        self.s_shape_11(x, y)

    def cg(self, x, y):
        self.moveTo(x + self.A, y + self.S)
        self.lineTo(x + self.A, y)
        self.moveTo(x + self.B, y + self.S)
        self.lineTo(x + self.B, y)

        self.moveTo(x, y + self.A)
        self.lineTo(x + self.A, y + self.A)
        self.moveTo(x, y + self.B)
        self.lineTo(x + self.A, y + self.B)

        self.moveTo(x + self.S, y + self.A)
        self.lineTo(x + self.B, y + self.A)
        self.moveTo(x + self.S, y + self.B)
        self.lineTo(x + self.B, y + self.B)

    def ch(self, x, y):
        self.moveTo(x, y + self.B)
        self.lineTo(x + self.S, y + self.B)
        self.moveTo(x, y + self.A)
        self.lineTo(x + self.S, y + self.A)

        self.moveTo(x + self.A, y + self.A)
        self.lineTo(x + self.A, y)
        self.moveTo(x + self.A, y + self.B)
        self.lineTo(x + self.A, y + self.S)

        self.moveTo(x + self.B, y + self.A)
        self.lineTo(x + self.B, y)
        self.moveTo(x + self.B, y + self.B)
        self.lineTo(x + self.B, y + self.S)


def render(grid, options):
    svg = SVG(grid, options)
    return svg.image()
