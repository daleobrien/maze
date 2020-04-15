/*jslint
    es6
*/
'use strict';

const Pi = Math.PI;
const Pi1_2 = Pi / 2;
const Pi3_2 = 3 * Pi / 2;
const Pi2 = 2 * Pi;
/* eslint-disable */
const W = ${width};
const H = ${height};
const A = ${a};
const A2 = ${a2};
const B = ${b};
const B2 = ${b2};
const G = ${g};
const n = ${n};
const R = ${r};
const R2 = ${r2};
const R3 = ${r3};
const R4 = ${r4};
const S = ${s};
const S2 = ${s2};
const Q = ${q};
const V = ${v};
const D = ${delta};
const T = ${theta};
${s_x_s};
${s_y_s};
/* eslint-enable */

let i = 0;
let j = H - 1;

class SVG {
  // Way to generate SVG using the same inteface we used with A JS Canvas
  constructor(colour, stroke_width, opacity) {
    this.svg = '';
    this.dots = '';
    this.colour = colour;
    this.stroke_width = stroke_width;
    this.opacity = opacity;
  }

  path() {
    return [
      '<path opacity="', this.opacity, '", stroke-width="', this.stroke_width,
      '" stroke="', this.colour, '" d="', this.svg, ' "></path>', this.dots
    ].join('')
  };

  dot(x, y, radius = S / 3) {
    const _x = x + S2;
    const _y = y + S2;

    this.dots += '<circle cx="' + _x + '" cy="' + _y + '" r="' + radius +
        '" fill-opacity="1.0" stroke-opacity="0" fill="#E51919" />';
  };

  posAngle(angle) {
    return angle < 0 ? angle + Pi2 : angle
  };

  polar(x, y, radius, angle) {
    return [x + (radius * Math.cos(angle)), y + (radius * Math.sin(angle))]
  };

  a(x, y, radius, startAngle, endAngle, dir = 1) {
    const _s = this.posAngle(startAngle);
    const _e = this.posAngle(endAngle);

    const [a, b] = this.polar(x, y, radius, _s);
    const [c, d] = this.polar(x, y, radius, _e);

    const diff = _e - _s;
    const large = 0 < diff && diff <= Pi ? 1 - dir : dir;

    this.svg += [
      'L', a, ' ', b, ' A', radius, ' ', radius, ' 0 ', large, ' ', dir, ' ', c,
      ' ', d, ' '
    ].join('');
  };

  m(x, y) {
    this.svg += ['M', x, ' ', y, ' '].join('')
  };
  l(x, y) {
    this.svg += ['L', x, ' ', y, ' '].join('')
  };

  ml(a, b, c, d) {
    this.m(a, b);
    this.l(c, d);
  };

  mh(a, b, x) {
    this.ml(a, b, a + x, b)
  };
  mv(a, b, y) {
    this.ml(a, b, a, b + y)
  };

  h(x, y, v) {
    this.ml(x, y + v, x + S, y + v)
  };
  v(x, y, h) {
    this.ml(x + h, y, x + h, y + S)
  };
};

// Maze walls
let p = new SVG('#000000', 2, '1.0');
// Trail
let t = new SVG('#E51919', 5, '1.0');
// Faint
let f = new SVG('#E51919', 5, '0.1');


const s0 = (x, y, radius = A) => {
  // ┘
  p.m(x + A, y);
  p.a(x, y, radius, 0, Pi1_2);
};

const s1 = (x, y, radius = A) => {
  // ┐
  p.m(x, y + B);
  p.a(x, y + S, radius, Pi3_2, Pi2);
};

const s2 = (x, y, radius = A) => {
  // └
  p.m(x + S, y + A);
  p.a(x + S, y, radius, Pi1_2, Pi);
};

const s3 = (x, y, radius = A) => {
  // ┌
  p.m(x + B, y + S);
  p.a(x + S, y + S, radius, Pi, Pi3_2);
};



const c1 = (x, y) => {
  // │ │
  // └─┘
  p.mv(x + B, y, Q);
  p.a(x + S - V, y + n + R, R, Pi, Pi + D, 0);
  p.a(x + S2, y + S2, S2 - G / 2, T - Pi1_2, Pi3_2 - T);
  p.a(x + V, y + n + R, R, Pi1_2 - T, Pi3_2 + T - D, 0);
  p.l(x + G, y);
};

const t1 = (x, y) => {
  // │
  // .
  t.mv(x + S2, y, S2);
};

const c2 = (x, y) => {
  // ┌─┐
  // │ │
  p.m(x + B, y + S);
  p.a(x + S - V, y + S - n - R, R, Pi, Pi - D);
  p.a(x + S2, y + S2, S2 - G / 2, Pi1_2 - T, T - Pi3_2, 0);
  p.a(x + V, y + S - n - R, R, Pi3_2 + T, Pi3_2 + T - D);
  p.l(x + A, y + S);
};

const t2 = (x, y) => {
  // .
  // │
  t.mv(x + S2, y + S, -S2);
};

const c4 = (x, y) => {
  // ┌──
  // └──
  p.m(x + S, y + B);
  p.a(x + S - n - R, y + S - V, R, Pi3_2, Pi3_2 + D, 0);
  p.a(x + S2, y + S2, S2 - G / 2, Pi1_2 + D, Pi1_2 + D - 2 * T);
  p.a(x + S - n - R, y + V, R, Pi - T, Pi - T + D, 0);
  p.l(x + S, y + A);
};

const t4 = (x, y) => {
  // .-
  t.mh(x + S, y + S2, -S2);
};

const c8 = (x, y) => {
  // ──┐
  // ──┘
  p.m(x, y + B);
  p.a(x + n + R, y + S - V, R, Pi3_2, Pi3_2 - D);
  p.a(x + S2, y + S2, S2 - G / 2, Pi1_2 - D, Pi1_2 - D + 2 * T, 0);
  p.a(x + n + R, y + V, R, T, T - D);
  p.l(x, y + A);
};

const t8 = (x, y) => {
  // -.
  t.mh(x, y + S2, S2);
};

const c5 = (x, y) => {
  // │ └
  // └──
  // Small arc
  s2(x, y);

  // Big arc
  p.m(x + S, y + B);
  p.a(x + B, y + A, R2, Pi1_2, Pi);
  p.l(x + A, y);
};

const t5 = (x, y) => {
  // Medium arc
  // └─
  t.m(x + S, y + S2);
  t.a(x + B2, y + A2, R3, Pi1_2, Pi);
  t.l(x + S2, y)
};

const c6 = (x, y) => {
  // ┌──
  // │ ┌
  s3(x, y);
  p.m(x + S, y + A);
  p.a(x + B, y + B, R2, Pi3_2, Pi, 0);
  p.l(x + A, y + S);
};

const t6 = (x, y) => {
  // ┌─
  t.m(x + S, y + S2);
  t.a(x + B2, y + B2, R3, Pi3_2, Pi, 0);
  t.l(x + S2, y + S);
};

const c9 = (x, y) => {
  // ┘ │
  // ──┘
  s0(x, y);
  p.m(x + B, y);
  p.a(x + A, y + A, R2, 0, Pi1_2);
  p.l(x, y + B);
};

const t9 = (x, y) => {
  // ─┘
  t.m(x + S2, y);
  t.a(x + A2, y + A2, R3, 0, Pi1_2);
  t.l(x, y + S2);
};

const ca = (x, y) => {
  // ──┐
  // ┐ │
  s1(x, y);
  p.m(x, y + A);
  p.a(x + A, y + B, R2, Pi3_2, Pi2);
  p.l(x + B, y + S);
};

const ta = (x, y) => {
  // ─┐
  t.m(x, y + S2);
  t.a(x + A2, y + B2, R3, Pi3_2, Pi2);
  t.l(x + S2, y + S);
};

const c7 = (x, y) => {
  // │ └
  // │ ┌
  p.v(x, y, A);
  s2(x, y);
  s3(x, y);
};



const cb = (x, y) => {
  // ┘ │
  // ┐ │
  p.v(x, y, B);
  s0(x, y);
  s1(x, y);
};

const c3 = (x, y) => {
  // │ │
  // │ │
  p.v(x, y, A);
  p.v(x, y, B);
};

const t3 = (x, y) => {
  // │
  // │
  t.v(x, y, S2);
};

const cc = (x, y) => {
  // ───
  // ───
  p.h(x, y, A);
  p.h(x, y, B);
};

const tc = (x, y) => {
  // ───
  t.h(x, y, S2);
};

const cd = (x, y) => {
  // ┘ └
  // ───
  p.h(x, y, B);
  s0(x, y);
  s2(x, y);
};

const ce = (x, y) => {
  // ───
  // ┐ ┌
  p.h(x, y, A);
  s1(x, y);
  s3(x, y);
};

const cf = (x, y) => {
  // ┘ └
  // ┐ ┌
  s0(x, y);
  s1(x, y);
  s2(x, y);
  s3(x, y);
};


const cg = (x, y) => {
  // ┤ ├
  // ┤ ├
  p.v(x, y, A);
  p.v(x, y, B);

  p.mh(x, y + A, A);
  p.mh(x, y + B, A);

  p.mh(x + S, y + A, B - S);
  p.mh(x + S, y + B, B - S);
};

const tg = (x, y) => {
  // Outside to A/B
  t.mh(x, y + S2, A);
  t.mh(x + S, y + S2, -A);
  // Inside to A/B
  f.mh(x + A, y + S2, R4);
  f.mh(x + B, y + S2, -R4);
};

const ch = (x, y) => {
  // ┴─┴
  // ┬─┬
  p.h(x, y, A);
  p.h(x, y, B);

  p.mv(x + A, y, A);
  p.mv(x + B, y, A);

  p.mv(x + A, y + B, S - B);
  p.mv(x + B, y + B, S - B);
};

const th = (x, y) => {
  // Outside to A/B
  t.mv(x + S2, y, A);
  t.mv(x + S2, y + S, -A);
  // Inside to A/B
  f.mv(x + S2, y + A, R4);
  f.mv(x + S2, y + B, -R4);
};

// Can skip over some since there is no choice
const NEXT_KEYCODE = {
  ArrowDown: {
    c5: 'ArrowRight',
    c9: 'ArrowLeft',
    c3: 'ArrowDown',
    cg: 'ArrowDown',
    ch: 'ArrowDown'
  },
  'ArrowUp': {
    c6: 'ArrowRight',
    ca: 'ArrowLeft',
    c3: 'ArrowUp',
    cg: 'ArrowUp',
    ch: 'ArrowUp'
  },
  ArrowRight: {
    c9: 'ArrowUp',
    ca: 'ArrowDown',
    cg: 'ArrowRight',
    cc: 'ArrowRight',
    ch: 'ArrowRight'
  },
  ArrowLeft: {
    c5: 'ArrowUp',
    c6: 'ArrowDown',
    cg: 'ArrowLeft',
    cc: 'ArrowLeft',
    ch: 'ArrowLeft'
  }
};
/*
  c1 │ │   c2 ┌─┐   c4 ┌──   c8   ──┐  c5 │ └   c6  ┌──  c9  ┘ │  ca  ──┐
     └─┘      │ │      └──        ──┘     └──       │ ┌      ──┘      ┐ │


  c7  │ └  cb  ┘ │  cd  ┘ └  ce  ───   c3  │ │  cg ─┤ ├─
      │ ┌      ┐ │      ───      ┐ ┌       │ │     ─┤ ├─


  cc  ───  ch ─┴─┴─   cf  ─┘ └─
      ───     ─┬─┬─       ─┐ ┌─

*/

// from direction , to direction
const TRAIL_CELLS = {
  't': {'l': t9, 'r': t5, 'b': t3},
  'l': {'t': t9, 'r': tc, 'b': ta},
  'r': {'l': tc, 't': t5, 'b': t6},
  'b': {'l': ta, 'r': t6, 't': t3}
};
const TRAIL_LAST = {
  'r': t4,
  'l': t8,
  'b': t2,
  't': t1
};
const SINGLES = new Set([c5, c6, c9, ca, cc, c3, cg, ch]);
// Moving out of
const UPS = new Set([c1, c5, c9, c7, cb, cd, cg, ch, c3, cf]);
const DOWNS = new Set([c2, c6, ca, c7, cb, ce, cg, ch, c3, cf]);
const RIGHTS = new Set([c4, c5, c6, c7, cc, cd, ce, cg, ch, cf]);
const LEFTS = new Set([c8, c9, ca, cb, cc, cd, ce, cg, ch, cf]);

let trail = [[0, H - 1]];

const direction = (dx, dy) => {
  if (dx == 0) {
    return dy == -1 ? 'b' : 't';
  }
  return dx == -1 ? 'r' : 'l';
};

${grid};
const process_key_code =
    (key_code) => {
      let a = i;
      let b = j;

      let from_set;
      let to_set;

      switch (key_code) {
        case 'ArrowDown':
          b = j < H - 1 ? j + 1 : j;
          from_set = DOWNS;
          to_set = UPS;
          break;

        case 'ArrowUp':
          b = j > 0 ? j - 1 : j;
          from_set = UPS;
          to_set = DOWNS;
          break;

        case 'ArrowRight':
          a = i < W - 1 ? i + 1 : i;
          from_set = RIGHTS;
          to_set = LEFTS;
          break;

        case 'ArrowLeft':
          a = i > 0 ? i - 1 : i;
          from_set = LEFTS;
          to_set = RIGHTS;
          break;
      }

      if (a == i && b == j) {
        return false
      }

      // Check that we can move this way
      const prev_cell = grid[j][i];
      const next_cell = grid[b][a];
      if (!from_set.has(prev_cell) || !to_set.has(next_cell)) {
        return false
      }

      i = a;
      j = b;
      if ((trail.length > 1) && trail.slice(-2)[0][0] == i &&
          trail.slice(-2)[0][1] == j) {
        trail = trail.slice(0, trail.length - 1);
      } else {
        trail.push([i, j]);
      }

      if (i == W - 1 && j == 0) {
        return false;
      }
      if (SINGLES.has(next_cell)) {
        return NEXT_KEYCODE[key_code][next_cell.name];
      }
      return false;
    }

const processMovement = (key_code) => {
  let code = key_code;
  while (code) {
    code = process_key_code(code);
  }

  // Render
  t.svg = '';
  t.dots = ''
  f.svg = '';

  if (trail.length > 1) {
    for (let idx = 0; idx < trail.length; idx++) {
      // current
      const [x, y] = trail[idx];

      if (idx == trail.length - 1) {
        // last cell
        const [x_p, y_p] = trail[idx - 1];
        const from_d = direction(x - x_p, y - y_p);
        TRAIL_LAST[from_d](x * S, y * S);
        ;
        t.dot(x * S, y * S, S / 5);

      } else {
        const [x_n, y_n] = trail[idx + 1];

        if (idx == 0) {
          // First cell
          if (x == x_n) {
            t1(x * S, y * S);
          } else {
            t4(x * S, y * S);
          }
        } else {
          const [x_p, y_p] = trail[idx - 1];
          const from_d = direction(x - x_p, y - y_p);
          const to_d = direction(x - x_n, y - y_n);

          const t_cell = TRAIL_CELLS[from_d][to_d];
          const current_cell = grid[y][x];
          if (t_cell == tc && current_cell == cg) {
            tg(x * S, y * S);
          } else if (t_cell == t3 && current_cell == ch) {
            th(x * S, y * S);
          } else {
            t_cell(x * S, y * S)
          }
        }
      }
    }
  }

  let c = document.getElementById('maze');
  c.innerHTML = f.path() + t.path() + p.path();
};


const drawShape = () => {
  let c = document.getElementById('maze');

  c.setAttribute('width', W * S);
  c.setAttribute('height', H * S);

  document.getElementById('inner').setAttribute(
      'style', 'height:' + H * S + 'px;width:' + W * S + 'px');

  const I = x_s.length;
  const J = y_s.length;

  for (let _j = 0; _j < J; _j++) {
    for (let _i = 0; _i < I; _i++) {
      if ((_i != 0 || _j != J - 1) && (_i != I - 1 || _j != 0)) {
        grid[_j][_i](x_s[_i], y_s[_j]);
      }
    }
  }

  p.dot(x_s[0], y_s[y_s.length - 1]);
  p.dot(x_s[x_s.length - 1], y_s[0]);

  c.innerHTML = f.path() + t.path() + p.path();

  document.body.onkeydown = (e) => processMovement(e.code);
};