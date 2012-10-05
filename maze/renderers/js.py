from math import sqrt, asin, pi, ceil


# generate some js for a html
def render(grid, options):

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
    #stroke = s / 7.0

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
    b = s - g

    TILES = {1: 'c1',
             2: 'c2',
             3: 'c3',
             4: 'c4',
             5: 'c5',
             6: 'c6',
             7: 'c7',
             8: 'c8',
             9: 'c9',
             10: 'c10',
             11: 'c11',
             12: 'c12',
             13: 'c13',
             14: 'c14',
             15: 'c15',
             19: 'c19',
             28: 'c28'}

    js = ""
    for j, row in enumerate(grid):
        # upper/lower rows
        for i, cell in enumerate(row):

            x = left_margin + i * s
            y = top_margin + j * s

            start = False
            end = False
            if (i == 0 and j == height - 1):
                start = True

            if (i == width - 1 and j == 0):
                end = True

            js += ("%s(p,%.2f,%.2f,%s,%.2f,%.2f,%.2f," +
                   "%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%d,%d);") % (
                                       TILES[cell],
                                       x,
                                       y,
                                       str(draw_with_curves),
                                       a, b, g, n, r, s, q, v, delta,
                                       theta, start, end)

    html_content = '''

    function*drawShape(){

        var*canvas = document.getElementById('maze');

        if (canvas.getContext){

            var*p = canvas.getContext('2d');
            p.beginPath();
            %s
            p.stroke();

        } else {
            alert('You*need*a*better*browser.*Try*Chrome.');
        }

    }''' % js

    # squeeze it down a little
    for key, value in ((" ", ""),
                       ("0.000000,", "0,"),
                       ("0.00,", "0,"),
                       ("0.00,", "0,"),
                       ("\n", ""),
                       ("*", " ")):
        html_content = html_content.replace(key, value)

    return html_content

#
