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
const B = ${b};
const G = ${g};
const n = ${n};
const R = ${r};
const S = ${s};
const S2 = ${s2};
const Q = ${q};
const V = ${v};
const D = ${delta};
const T = ${theta};
${s_x_s};
${s_y_s};
/* eslint-enable */

class SVG {
  // Way to generate SVG using the same inteface we used with A JS Canvas
  constructor() {
    this.svg = '';
    this.track = '';
    this.dots = '';
  }

  path = () =>
      '<path stroke-linecap="round" d="' + this.svg + '  "></path>' + this.dots;

  dot = (x, y) => {
    const _x = x + S2;
    const _y = y + S2;

    this.dots += '<circle cx="' + _x + '" cy="' + _y + '" r="' + S / 3 +
        '" fill-opacity="1.0" stroke-opacity="0" fill="#E51919" />';
  };

  posAngle = (angle) => angle < 0 ? angle + Pi2 : angle;

  polar = (x, y, radius, angle) =>
      [x + (radius * Math.cos(angle)), y + (radius * Math.sin(angle))];

  a = (x, y, radius, startAngle, endAngle, dir = 1) => {
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

  m = (x, y) => this.svg += ['M', x, ' ', y, ' '].join('');
  l = (x, y) => this.svg += ['L', x, ' ', y, ' '].join('');

  ml = (a, b, c, d) => {
    this.m(a, b);
    this.l(c, d);
  };

  mh = (a, b, x) => this.ml(a, b, a + x, b);
  mv = (a, b, y) => this.ml(a, b, a, b + y);

  h = (x, y, v) => this.ml(x, y + v, x + S, y + v);
  v = (x, y, h) => this.ml(x + h, y, x + h, y + S);
};

let p = new SVG();

const s0 = (x, y) => {
  p.m(x + A, y);
  p.a(x, y, A, 0, Pi1_2);
  p.l(x, y + A);
};

const s1 = (x, y) => {
  p.m(x, y + B);
  p.a(x, y + S, A, Pi3_2, Pi2);
  p.l(x + A, y + S);
};

const s2 = (x, y) => {
  p.m(x + S, y + A);
  p.a(x + S, y, A, Pi1_2, Pi);
  p.l(x + B, y);
};

const s3 = (x, y) => {
  p.m(x + S, y + B);
  p.a(x + S, y + S, A, Pi3_2, Pi, 0);
  p.l(x + B, y + S);
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

const c2 = (x, y) => {
  // ┌─┐
  // │ │
  p.m(x + B, y + S);
  p.a(x + S - V, y + S - n - R, R, Pi, Pi - D);
  p.a(x + S2, y + S2, S2 - G / 2, Pi1_2 - T, T - Pi3_2, 0);
  p.a(x + V, y + S - n - R, R, Pi3_2 + T, Pi3_2 + T - D, 1);
  p.l(x + A, y + S);
};

const c3 = (x, y) => {
  // │ │
  // │ │
  // p.mv(x + A, y, S);
  // p.mv(x + B, y, S);
  p.v(x, y, A);
  p.v(x, y, B);
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


const c5 = (x, y) => {
  // │ └
  // └──
  s2(x, y);
  p.m(x + S, y + B);
  p.a(x + B, y + A, B - A, Pi1_2, Pi);
  p.l(x + A, y);
};

const c6 = (x, y) => {
  // ┌──
  // │ ┌
  s3(x, y);
  p.m(x + S, y + A);
  p.a(x + A + B, y + A + B, B, Pi3_2, Pi, 0);
  p.l(x + A, y + S);
};

const c7 = (x, y) => {
  // │ └
  // │ ┌
  p.v(x, y, A);
  s2(x, y);
  s3(x, y);
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

const c9 = (x, y) => {
  // ┘ │
  // ──┘
  s0(x, y);
  p.m(x + B, y);
  p.a(x + A, y + A, B - A, 0, Pi1_2);
  p.l(x, y + B);
};

const ca = (x, y) => {
  // ──┐
  // ┐ │
  s1(x, y);
  p.m(x, y + A);
  p.a(x + A, y + B, B - A, Pi3_2, Pi2);
  p.l(x + B, y + S);
};

const cb = (x, y) => {
  // ┘ │
  // ┐ │
  p.v(x, y, B);
  s0(x, y);
  s1(x, y);
};

const cc = (x, y) => {
  // ───
  // ───
  p.h(x, y, A);
  p.h(x, y, B);
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

const drawShape = () => {
  let c = document.getElementById('maze');

  c.setAttribute('width', W * S + S);
  c.setAttribute('height', H * S + S);

  document.getElementById('inner').setAttribute(
      'style', 'width:' + W * S + 'px');

  const I = x_s.length;
  const J = y_s.length;

  ${grid};

  for (let j = 0; j < J; j++) {
    for (let i = 0; i < I; i++) {
      if ((i != 0 || j != J - 1) && (i != I - 1 || j != 0)) {
        grid[j][i](x_s[i], y_s[j]);
      }
    }
  }

  p.dot(x_s[0], y_s[y_s.length - 1]);
  p.dot(x_s[x_s.length - 1], y_s[0]);

  c.innerHTML = p.path();
};