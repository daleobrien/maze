# -*- coding: utf-8 -*-

from math import sqrt, asin, pi, ceil
from reportlab.pdfgen.canvas import Canvas
from StringIO import StringIO


# generate pdf
def render(grid, options):

    draw_with_curves = options['draw_with_curves']
    filename = options['filename']

    use_A4 = options['use_A4']
    width = options['width']
    height = options['height']

    def s_shape_00(p):
        p.moveTo(a, 0)
        if draw_with_curves:
            p.arcTo(-a, -a, a, a, 0, 90)
        else:
            p.lineTo(a, a)
        p.lineTo(0, a)

    def s_shape_01(p):
        p.moveTo(0, b)
        if draw_with_curves:
            p.arcTo(-a, b, a, s + a, 270, 90)
        else:
            p.lineTo(a, b)
        p.lineTo(a, s)

    def s_shape_10(p):
        p.moveTo(s, a)
        if draw_with_curves:
            p.arcTo(b, -a, s + a, a, 90, 90)
        else:
            p.lineTo(b, a)
        p.lineTo(b, 0)

    def s_shape_11(p):
        p.moveTo(s, b)
        if draw_with_curves:
            p.arcTo(b, b, s + a, s + a, 270, -90)
        else:
            p.lineTo(b, b)
        p.lineTo(b, s)

    buffer = StringIO()
    if filename:
        c = Canvas(filename)
    else:
        c = Canvas(buffer)

    c.setTitle('Maze')
    c.setSubject("")
    c.setAuthor("Dale O'Brien")

    if use_A4:
        page_width = 8.3 * 72
        page_height = 11.7 * 72
    else:
        page_width = 8.5 * 72
        page_height = 11.0 * 72

    c.setPageSize((page_width, page_height))

    # 0=butt,1=draw_with_curves,2=square
    c.setLineCap(1)

    left_margin = 15
    top_margin = 15

    # cells must be square, it's the math!, I'm not doing it again.
    # so scale the width if the height will go over the page

    org_width = width
    ratio = (page_height - 2 * top_margin) / (page_width - 2 * left_margin)
    if (float(height) / width > ratio):
        width = ceil(height / ratio)

    s = (page_width - 2 * left_margin) / width

    # center the maze, looks better for mazes that don't fit the page nicely
    left_margin -= (org_width - width) * s / 2.0
    top_margin -= (s * height - (page_height - 2.0 * top_margin)) / 2.0

    g = s * 0.2
    stroke = s / 7.0
    c.setLineWidth(stroke)

    k = 0.5

    n = -(g / k) + 0.5 * (s - sqrt((g *
        (4.0 * g - 3.0 * g * k + 2 * k * s)) / k))

    r = g / k
    q = n + r
    v = (g * (-1 + k)) / k

    theta = asin((2.0 * g - 2.0 * g * k + k * s) /
        (2.0 * g - g * k + k * s)) * 180 / pi

    delta = theta - 90

    for j, row in enumerate(grid):
        # upper/lower rows
        for i, cell in enumerate(row):

            x_offset = left_margin + i * s
            y_offset = top_margin + j * s

            c.translate(x_offset, y_offset)
            p = c.beginPath()

            a = g
            b = s - g

            # mark start and end
            start = False
            end = False
            if (i == 0 and j == height - 1):
                start = True

            if (i == width - 1 and j == 0):
                end = True

            if start or end:
                c.setStrokeColorRGB(0.9, 0.1, 0.1)
                c.setFillColorRGB(0.9, 0.1, 0.1)
                p.circle(s / 2.0, s / 2.0, g / 1.5)
                c.drawPath(p, fill=True)
                p = c.beginPath()
                c.setStrokeColorRGB(0.0, 0.0, 0.0)

            if cell == 3:

                '│ │'
                '│ │'

                p.moveTo(a, s)
                p.lineTo(a, 0)
                p.moveTo(b, s)
                p.lineTo(b, 0)

            if cell == 1:

                '│ │'
                '└─┘'

                p.moveTo(b, 0)
                if draw_with_curves:

                    p.lineTo(b, q)
                    x = s - v - r
                    y = n
                    p.arcTo(x, y, x + 2 * r, y + 2 * r, 180, delta)

                    p.arcTo(g / 2,
                            g / 2,
                            s - g / 2,
                            s - g / 2, theta - 90, 360 - 2 * theta)

                    x = v - r
                    p.arcTo(x, y,
                            x + 2 * r,
                            y + 2 * r, 90 - theta, delta)

                else:
                    p.lineTo(b, b)
                    p.lineTo(a, b)
                p.lineTo(g, 0)

            if cell == 2:

                '┌─┐'
                '│ │'

                p.moveTo(b, s)
                if draw_with_curves:

                    x = s - v - r
                    y = s - n - 2 * r
                    p.arcTo(x, y, x + 2 * r, y + 2 * r, 180, -delta)

                    p.arcTo(g / 2,
                            g / 2,
                            s - g / 2,
                            s - g / 2, 90 - theta, -360 + 2 * theta)

                    x = v - r
                    p.arcTo(x, y,
                            x + 2 * r,
                            y + 2 * r, 270 + theta, -delta)

                else:
                    p.lineTo(b, a)
                    p.lineTo(a, a)
                p.lineTo(a, s)

            if cell == 4:

                '┌──'
                '└──'

                p.moveTo(s, b)
                if draw_with_curves:
                    x = s - n - 2 * r
                    y = s - v - r
                    p.arcTo(x, y, x + 2 * r, y + 2 * r, 270, delta)

                    p.arcTo(g / 2,
                            g / 2,
                            s - g / 2,
                            s - g / 2, 90 + delta, 360 - 2 * theta)

                    y = v - r
                    p.arcTo(x, y,
                            x + 2 * r,
                            y + 2 * r, 180 - theta, delta)

                else:
                    p.lineTo(g, b)
                    p.lineTo(a, a)
                p.lineTo(s, a)

            if cell == 8:

                '──┐'
                '──┘'

                p.moveTo(0, b)
                if draw_with_curves:
                    x = n
                    y = s - v - r

                    p.arcTo(x, y, x + 2 * r, y + 2 * r, 270, -delta)

                    p.arcTo(g / 2,
                            g / 2,
                            s - g / 2,
                            s - g / 2, 90 - delta, -360 + 2 * theta)

                    y = v - r
                    p.arcTo(x, y,
                            x + 2 * r,
                            y + 2 * r, theta, -delta)
                else:
                    p.lineTo(b, b)
                    p.lineTo(b, a)
                p.lineTo(0, a)

            if cell == 5:

                '│ └'
                '└──'

                s_shape_10(p)

                p.moveTo(s, b)
                if draw_with_curves:
                    if start:
                        p.arcTo(a, a, b, b, 90, 90)
                    else:
                        p.arcTo(a, 2 * a - b, 2 * b - a, b, 90, 90)
                else:
                    p.lineTo(a, b)
                p.lineTo(a, 0)

            if cell == 6:

                '┌──'
                '│ ┌'

                s_shape_11(p)

                p.moveTo(s, a)
                if draw_with_curves:
                    p.arcTo(a, a, 2 * b + a, 2 * b + a, 270, -90)
                else:
                    p.lineTo(a, a)
                p.lineTo(a, s)

            if cell == 7:

                '│ └'
                '│ ┌'

                p.moveTo(a, s)
                p.lineTo(a, 0)

                s_shape_10(p)
                s_shape_11(p)

            if cell == 9:

                '┘ │'
                '──┘'

                s_shape_00(p)

                p.moveTo(b, 0)
                if draw_with_curves:
                    p.arcTo(2 * a - b, 2 * a - b, b, b, 0, 90)
                else:
                    p.lineTo(b, b)
                p.lineTo(0, b)

            if cell == 10:

                '──┐'
                '┐ │'

                s_shape_01(p)

                p.moveTo(0, a)
                if draw_with_curves:
                    if end:
                        p.arcTo(a, a, b, b, 270, 90)
                    else:
                        p.arcTo(2 * a - b, a, b, 2 * b + a, 270, 90)
                else:
                    p.lineTo(b, a)
                p.lineTo(b, s)

            if cell == 11:

                '┘ │'
                '┐ │'

                p.moveTo(b, s)
                p.lineTo(b, 0)

                s_shape_00(p)
                s_shape_01(p)

            if cell == 12:

                '───'
                '───'

                p.moveTo(0, b)
                p.lineTo(s, b)
                p.moveTo(0, a)
                p.lineTo(s, a)

            if cell == 13:

                '┘ └'
                '───'

                p.moveTo(0, b)
                p.lineTo(s, b)

                s_shape_00(p)
                s_shape_10(p)

            if cell == 14:

                '───'
                '┐ ┌'

                p.moveTo(0, a)
                p.lineTo(s, a)

                s_shape_01(p)
                s_shape_11(p)

            if cell == 15:

                '┘ └'
                '┐ ┌'

                s_shape_00(p)
                s_shape_10(p)
                s_shape_01(p)
                s_shape_11(p)

            if cell == 19:

                '┤ ├'
                '┤ ├'

                p.moveTo(a, s)
                p.lineTo(a, 0)
                p.moveTo(b, s)
                p.lineTo(b, 0)

                p.moveTo(0, a)
                p.lineTo(a, a)
                p.moveTo(0, b)
                p.lineTo(a, b)

                p.moveTo(s, a)
                p.lineTo(b, a)
                p.moveTo(s, b)
                p.lineTo(b, b)

            if cell == 28:

                '┴─┴'
                '┬─┬'

                p.moveTo(0, b)
                p.lineTo(s, b)
                p.moveTo(0, a)
                p.lineTo(s, a)

                p.moveTo(a, a)
                p.lineTo(a, 0)
                p.moveTo(a, b)
                p.lineTo(a, s)

                p.moveTo(b, a)
                p.lineTo(b, 0)
                p.moveTo(b, b)
                p.lineTo(b, s)

            c.drawPath(p)
            c.translate(-x_offset, -y_offset)

    c.save()
    pdf = ""
    if not filename:
        pdf = buffer.getvalue()
        buffer.close()

    return pdf
